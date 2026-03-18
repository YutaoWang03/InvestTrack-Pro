from django.db.models import Sum, F, Q
from django.db import transaction
import json
from datetime import datetime, time, timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal
from .models import Security, Position, HistoryPrice, DailySnapshot, AccountSnapshot, Trade
from .utils.calculations import (
    calc_holding_period_return,
    calc_dynamic_annualized_return,
    calc_volatility,
    calc_sharpe_ratio,
    calc_max_drawdown,
    calc_var_historical,
    calc_cvar_historical,
    calc_bias,
    calc_atr,
    calc_stop_loss
)
from django.core.paginator import Paginator


def dashboard(request):
    # 1. 获取最新账户快照数据
    latest_acc = AccountSnapshot.objects.order_by('-date').first()
    if not latest_acc:
        return render(request, 'index.html', {'error': '暂无账户快照数据'})

    latest_date = latest_acc.date

    # 2. 从AccountSnapshot读取最新的总资产数据
    current_assets = float(latest_acc.total_equity)

    # 3. 从AccountSnapshot读取最新的涨跌数据
    daily_change = float(latest_acc.daily_pnl)

    # 4. 计算本月的盈亏
    # 获取本月第一天
    today = datetime.now().date()
    month_start = today.replace(day=1)
    # 计算本月所有daily_pnl的总和
    monthly_profit = AccountSnapshot.objects.filter(date__gte=month_start).aggregate(
        total_pnl=Sum('daily_pnl')
    )['total_pnl'] or 0
    monthly_profit = float(monthly_profit)

    # 5. 准备折线图数据 (日期 vs 每日总资产)
    # 从AccountSnapshot表获取数据
    history_data = AccountSnapshot.objects.order_by('date')

    line_labels = [item.date.strftime('%m-%d') for item in history_data]
    line_values = [float(item.total_equity) for item in history_data]

    # 6. 准备饼图数据 (资产大类分布)
    # 从DailySnapshot表获取数据，保持不变
    category_data = DailySnapshot.objects.filter(date=latest_date).values(
        'code__major_categories'
    ).annotate(
        cat_total=Sum(F('quantity') * F('close'))
    )

    pie_labels = [item['code__major_categories'] or '未分类' for item in category_data]
    pie_values = [float(item['cat_total']) for item in category_data]

    # 7. 计算风险指标
    account_history = AccountSnapshot.objects.order_by('date')[:60]  # Last 60 days
    equity_values = [float(s.total_equity) for s in account_history]
    equity_decimals = [Decimal(str(val)) for val in equity_values]

    # 计算组合最大回撤
    max_drawdown = float(calc_max_drawdown(equity_decimals)) * 100 if equity_decimals else 0

    # 计算风险敞口
    risk_exposure = 0
    if latest_acc:
        if float(latest_acc.total_equity) > 0:
            risk_exposure = (float(latest_acc.total_market_value) / float(latest_acc.total_equity)) * 100

    # 8. 从Position表读取持仓数据并计算相关指标
    positions = Position.objects.all()
    position_list = []
    total_market_value = 0
    
    for position in positions:
        # 获取最新收盘价
        latest_price = HistoryPrice.objects.filter(code=position.code).order_by('-date').first()
        current_price = float(latest_price.close) if latest_price else 0
        
        # 计算市值
        market_value = float(position.quantity) * current_price
        total_market_value += market_value
        
        # 计算持仓收益率
        if float(position.avg_cost) > 0:
            return_rate = (current_price - float(position.avg_cost)) / float(position.avg_cost) * 100
        else:
            return_rate = 0
        
        # 计算年化收益率
        # 假设持仓时间为30天，实际项目中应该根据买入时间计算
        annual_return = calc_dynamic_annualized_return(Decimal(str(return_rate)), 30)
        annual_return = float(annual_return) * 100
        
        # 添加到持仓列表
        position_list.append({
            'code': position.code,
            'current_price': current_price,
            'avg_cost': float(position.avg_cost),
            'return_rate': return_rate,
            'annual_return': annual_return,
            'market_value': market_value,
            'weight': 0  # 暂时设为0，后面计算
        })
    
    # 计算持仓占比
    for position in position_list:
        if total_market_value > 0:
            position['weight'] = (position['market_value'] / total_market_value) * 100
        else:
            position['weight'] = 0
    
    context = {
        'total_assets': round(current_assets, 2),
        'monthly_profit': round(monthly_profit, 2),
        'daily_change': round(daily_change, 2),
        'latest_date': latest_date,
        'latest_snapshot': latest_acc,
        'line_labels': json.dumps(line_labels),
        'line_values': json.dumps(line_values),
        'pie_labels': json.dumps(pie_labels),
        'pie_values': json.dumps(pie_values),
        'max_drawdown': round(max_drawdown, 2),
        'risk_exposure': round(risk_exposure, 2),
        'positions': position_list,
    }
    return render(request, 'index.html', context)