#!/usr/bin/env python
"""
创建示例数据脚本
用于测试InvestTrack系统功能
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, date, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.investments.models import Security, HistoryPrice, Position, Trade, AccountSnapshot, DailySnapshot
from apps.risk_engine.models import StrategyConfig


def create_sample_data():
    print("🚀 开始创建示例数据...")
    
    # 1. 创建证券信息
    securities_data = [
        {'code': '000001', 'name': '平安银行', 'category': 'stock', 'major_categories': 'equity', 'sector': '银行'},
        {'code': '000002', 'name': '万科A', 'category': 'stock', 'major_categories': 'equity', 'sector': '房地产'},
        {'code': '000858', 'name': '五粮液', 'category': 'stock', 'major_categories': 'equity', 'sector': '食品饮料'},
        {'code': '159919', 'name': '沪深300ETF', 'category': 'etf', 'major_categories': 'equity', 'sector': '指数基金'},
        {'code': '110003', 'name': '建信转债', 'category': 'fund', 'major_categories': 'bond', 'sector': '债券基金'},
        {'code': 'CASH00', 'name': '现金', 'category': 'cash', 'major_categories': 'currency', 'sector': '货币'},
    ]
    
    securities = []
    for data in securities_data:
        security, created = Security.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        securities.append(security)
        if created:
            print(f"✅ 创建证券: {security}")
    
    # 2. 创建历史行情数据（最近30天）
    print("📈 创建历史行情数据...")
    base_prices = {
        '000001': Decimal('12.50'),  # 平安银行
        '000002': Decimal('18.30'),  # 万科A
        '000858': Decimal('180.50'), # 五粮液
        '159919': Decimal('4.20'),   # 沪深300ETF
        '110003': Decimal('1.05'),   # 建信转债
    }
    
    for i in range(30):
        trade_date = date.today() - timedelta(days=i)
        
        for security in securities[:5]:  # 不为现金创建行情
            base_price = base_prices[security.code]
            # 模拟价格波动 (-3% 到 +3%)
            import random
            change_pct = (random.random() - 0.5) * 0.06  # -3% to +3%
            current_price = base_price * (1 + Decimal(str(change_pct)))
            
            # 计算OHLC
            high = current_price * Decimal('1.02')
            low = current_price * Decimal('0.98')
            open_price = current_price * (1 + Decimal(str((random.random() - 0.5) * 0.02)))
            
            # 计算成交量
            volume = Decimal(str(random.randint(100000, 1000000)))
            amount = current_price * volume
            
            # 计算技术指标（简化）
            ma_20 = current_price * Decimal('0.99')  # 简化的20日均线
            atr_20 = current_price * Decimal('0.02')  # 简化的ATR
            
            HistoryPrice.objects.get_or_create(
                date=trade_date,
                code=security,
                defaults={
                    'open': open_price,
                    'high': high,
                    'low': low,
                    'close': current_price,
                    'preclose': current_price * Decimal('0.99'),
                    'volume': volume,
                    'amount': amount,
                    'turn': Decimal('2.5'),
                    'ma_20': ma_20,
                    'atr_20': atr_20,
                }
            )
    
    # 3. 创建策略配置
    print("⚙️ 创建策略配置...")
    strategy_configs = [
        {'code': securities[0], 'strategy_type': 'LEFT', 'risk_percent': Decimal('0.01')},
        {'code': securities[1], 'strategy_type': 'RIGHT', 'risk_percent': Decimal('0.015')},
        {'code': securities[2], 'strategy_type': 'RIGHT', 'risk_percent': Decimal('0.02')},
        {'code': securities[3], 'strategy_type': 'LEFT', 'risk_percent': Decimal('0.01')},
    ]
    
    for config_data in strategy_configs:
        config, created = StrategyConfig.objects.get_or_create(
            code=config_data['code'],
            defaults=config_data
        )
        if created:
            print(f"✅ 创建策略配置: {config.code.name} - {config.strategy_type}")
    
    # 4. 创建持仓数据
    print("💼 创建持仓数据...")
    positions_data = [
        {'code': securities[0], 'quantity': Decimal('1000'), 'avg_cost': Decimal('12.00')},
        {'code': securities[1], 'quantity': Decimal('500'), 'avg_cost': Decimal('18.00')},
        {'code': securities[2], 'quantity': Decimal('100'), 'avg_cost': Decimal('175.00')},
        {'code': securities[3], 'quantity': Decimal('2000'), 'avg_cost': Decimal('4.10')},
        {'code': securities[5], 'quantity': Decimal('50000'), 'avg_cost': Decimal('1.00')},  # 现金
    ]
    
    for pos_data in positions_data:
        position, created = Position.objects.get_or_create(
            code=pos_data['code'],
            defaults=pos_data
        )
        if created:
            print(f"✅ 创建持仓: {position.code.name} - {position.quantity}股")
    
    # 5. 创建交易记录
    print("💰 创建交易记录...")
    trades_data = [
        {'code': securities[0], 'trade_type': 'BUY', 'trade_quantity': Decimal('1000'), 'total_amount': Decimal('12000')},
        {'code': securities[1], 'trade_type': 'BUY', 'trade_quantity': Decimal('500'), 'total_amount': Decimal('9000')},
        {'code': securities[2], 'trade_type': 'BUY', 'trade_quantity': Decimal('100'), 'total_amount': Decimal('17500')},
        {'code': securities[3], 'trade_type': 'BUY', 'trade_quantity': Decimal('2000'), 'total_amount': Decimal('8200')},
    ]
    
    for i, trade_data in enumerate(trades_data):
        trade_date = datetime.now() - timedelta(days=20-i*2)
        Trade.objects.get_or_create(
            date=trade_date,
            code=trade_data['code'],
            trade_type=trade_data['trade_type'],
            defaults={
                'trade_quantity': trade_data['trade_quantity'],
                'total_amount': trade_data['total_amount'],
                'fee': trade_data['total_amount'] * Decimal('0.0005'),
            }
        )
    
    # 6. 创建账户快照数据
    print("📊 创建账户快照数据...")
    base_equity = Decimal('100000')  # 10万初始资金
    
    for i in range(30):
        snapshot_date = date.today() - timedelta(days=i)
        
        # 模拟账户净值变化
        import random
        change_pct = (random.random() - 0.5) * 0.04  # -2% to +2%
        current_equity = base_equity * (1 + Decimal(str(change_pct * (30-i) / 30)))
        
        # 计算其他指标
        market_value = current_equity * Decimal('0.8')  # 80%仓位
        cash = current_equity - market_value
        daily_pnl = current_equity * Decimal(str(change_pct))
        
        AccountSnapshot.objects.get_or_create(
            date=snapshot_date,
            defaults={
                'total_equity': current_equity,
                'total_market_value': market_value,
                'available_cash': cash,
                'daily_pnl': daily_pnl,
                'daily_change_pct': Decimal(str(change_pct * 100)),
                'total_risk_exposure': Decimal('80.0'),
                'overall_position_ratio': Decimal('80.0'),
            }
        )
    
    # 7. 创建每日快照
    print("📸 创建每日快照数据...")
    for i in range(10):
        snapshot_date = date.today() - timedelta(days=i)
        
        for position in Position.objects.all():
            if position.code.code != 'CASH00':  # 不为现金创建快照
                latest_price = HistoryPrice.objects.filter(
                    code=position.code,
                    date=snapshot_date
                ).first()
                
                if latest_price:
                    DailySnapshot.objects.get_or_create(
                        date=snapshot_date,
                        code=position.code,
                        defaults={
                            'quantity': position.quantity,
                            'close': latest_price.close,
                        }
                    )
    
    print("✅ 示例数据创建完成！")
    print("\n📊 数据统计:")
    print(f"证券信息: {Security.objects.count()} 条")
    print(f"历史行情: {HistoryPrice.objects.count()} 条")
    print(f"持仓记录: {Position.objects.count()} 条")
    print(f"交易记录: {Trade.objects.count()} 条")
    print(f"账户快照: {AccountSnapshot.objects.count()} 条")
    print(f"每日快照: {DailySnapshot.objects.count()} 条")
    print(f"策略配置: {StrategyConfig.objects.count()} 条")
    print("\n🌐 现在可以访问 http://127.0.0.1:8000/ 查看数据了！")


if __name__ == '__main__':
    create_sample_data()