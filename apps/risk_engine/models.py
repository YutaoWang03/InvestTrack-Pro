from django.db import models
from decimal import Decimal


# 策略配置表
class StrategyConfig(models.Model):
    STRATEGY_CHOICES = [('LEFT', '左侧埋伏'), ('RIGHT', '右侧趋势')]
    code = models.ForeignKey('investments.Security', on_delete=models.CASCADE, to_field='code', db_column='code',
                             verbose_name="标的代码")
    strategy_type = models.CharField(max_length=10, choices=STRATEGY_CHOICES, default='RIGHT', verbose_name="交易模式")
    risk_percent = models.DecimalField(max_digits=5, decimal_places=4, default=0.0100, verbose_name="单笔风险系数 (%)")
    max_position_weight = models.DecimalField(max_digits=5, decimal_places=4, default=0.2000,
                                              verbose_name="仓位上限 (%)")
    atr_period = models.IntegerField(default=20, verbose_name="ATR 计算周期")
    stop_loss_multiplier = models.DecimalField(max_digits=3, decimal_places=1, default=2.0,
                                               verbose_name="止损 ATR 倍数")
    bias_threshold = models.DecimalField(max_digits=5, decimal_places=4, default=0.1500,
                                         verbose_name="乖离率减仓阈值 (%)")
    is_active = models.BooleanField(default=True, verbose_name="策略是否启用")
    note = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = "交易策略"
        verbose_name_plural = "策略配置列表"
