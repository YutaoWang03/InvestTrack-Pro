from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from decimal import Decimal


# 1. 证券信息表
class Security(models.Model):
    CATEGORY_CHOICES = [('stock', '股票'), ('fund', '基金'), ('etf', 'ETF'), ('cash', '现金')]
    MAJOR_CHOICES = [('equity', '权益'), ('bond', '债券'), ('currency', '货币'), ('commodity', '大宗商品')]

    code = models.CharField("证券代码", max_length=6, primary_key=True,
                            validators=[MinLengthValidator(6), MaxLengthValidator(6)])
    name = models.CharField("名称", max_length=100)

    # 添加默认值
    category = models.CharField("资产类别", max_length=10, choices=CATEGORY_CHOICES, default='fund')
    major_categories = models.CharField("资产大类", max_length=20, choices=MAJOR_CHOICES, default='equity', blank=True)
    sector = models.CharField("投资行业", max_length=50, default="未分类", blank=True)

    class Meta:
        verbose_name = "标的信息"

    def __str__(self):
        return f"{self.name} ({self.code})"


# 2. 历史行情表
class HistoryPrice(models.Model):
    history_id = models.AutoField(primary_key=True)
    date = models.DateField("日期")
    code = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='history_prices', to_field='code')

    # 给价格和成交量添加 0 默认值
    open = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    high = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    low = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    close = models.DecimalField("收盘价", max_digits=20, decimal_places=4, default=0)
    preclose = models.DecimalField("昨收价", max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField("成交量", max_digits=20, decimal_places=2, default=0)
    amount = models.DecimalField("成交额", max_digits=20, decimal_places=2, default=0)
    turn = models.DecimalField("换手率", max_digits=10, decimal_places=4, default=0)
    adjustflag = models.IntegerField("复权因子", default=1)

    atr_20 = models.DecimalField("20日ATR", max_digits=20, decimal_places=4, default=0, blank=True)
    ma_20 = models.DecimalField("20日均线", max_digits=20, decimal_places=4, default=0, blank=True)

    class Meta:
        unique_together = ('date', 'code')
        verbose_name = "历史行情"
        verbose_name_plural = "历史行情列表"
        indexes = [models.Index(fields=['code', 'date'])]


# 3. 当前持仓表
class Position(models.Model):
    code = models.OneToOneField('Security', on_delete=models.CASCADE, primary_key=True, to_field='code')
    quantity = models.DecimalField("持有数量", max_digits=20, decimal_places=4, default=0)
    avg_cost = models.DecimalField("平均持仓成本", max_digits=20, decimal_places=4, default=0)
    strategy_label = models.CharField("关联策略标识", max_length=20, default="LEFT", blank=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "当前持仓"


# 4. 资产快照表
class DailySnapshot(models.Model):
    snapshot_id = models.AutoField(primary_key=True)
    date = models.DateField("快照日期")
    code = models.ForeignKey(Security, on_delete=models.CASCADE, to_field='code')
    quantity = models.DecimalField("当日持有数量", max_digits=20, decimal_places=4, default=0)
    close = models.DecimalField("当日结算价", max_digits=20, decimal_places=4, default=0)

    class Meta:
        unique_together = ('date', 'code')
        verbose_name = "历史持仓"


# 5. 交易记录表
class Trade(models.Model):
    trade_id = models.AutoField(primary_key=True)
    date = models.DateTimeField("交易时间")
    code = models.ForeignKey(Security, on_delete=models.CASCADE, to_field='code')
    trade_quantity = models.DecimalField("交易数量", max_digits=20, decimal_places=4, default=0)
    fee = models.DecimalField("手续费", max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField("成交总金额", max_digits=20, decimal_places=2, default=0)
    trade_type = models.CharField("交易类型", max_length=10, default="BUY")
    remark = models.TextField("备注", default="", blank=True)


# 7. 账户每日净值快照表
class AccountSnapshot(models.Model):
    date = models.DateField("日期", primary_key=True)
    total_equity = models.DecimalField("总资产", max_digits=20, decimal_places=2, default=0)
    total_market_value = models.DecimalField("总市值", max_digits=20, decimal_places=2, default=0)
    available_cash = models.DecimalField("可用现金", max_digits=20, decimal_places=2, default=0)
    daily_pnl = models.DecimalField("当日盈亏", max_digits=20, decimal_places=2, default=0)
    daily_change_pct = models.DecimalField("前日涨跌幅 (%)", max_digits=10, decimal_places=4, default=0)
    total_risk_exposure = models.DecimalField("总体风险敞口 (%)", max_digits=10, decimal_places=4, default=0)
    tolerant_risk_exposure = models.DecimalField("可容忍风险敞口 (%)", max_digits=10, decimal_places=4, default=8.0)

    overall_position_ratio = models.DecimalField("整体仓位比例 (%)", max_digits=10, decimal_places=4, default=0)

    class Meta:
        verbose_name = "每日净值"
        ordering = ['-date']