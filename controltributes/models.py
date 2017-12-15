from django.db import models
from accounts.models import User
from cuser.middleware import CuserMiddleware
from django.contrib.sessions.models import Session


class Tribute(models.Model):
	description = models.CharField('Descrição', max_length=50,
		help_text="No máximo 50 caractéres")
	period = models.CharField('Período de Pagamento', max_length=200,
		help_text="No máximo 200 caractéres")
	user = models.ForeignKey(User,
		on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.description

	@staticmethod
	def getTributes(user_id):
		return Tribute.objects.filter(user_id=user_id)

	@staticmethod
	def getTributeChoices(user_id):
		sql = """
		SELECT id, description FROM controltributes_tribute 
		WHERE user_id = {}
		""".format(user_id)
		return Tribute.objects.raw(sql)

class Payment(models.Model):
	from datetime import date
	value = models.DecimalField('Valor R$', max_digits=5,
		decimal_places=2)
	date = models.DateField('Pago em', default=date.today, editable=False)
	tribute = models.ForeignKey(Tribute, on_delete=models.CASCADE)

	def __str__(self):
		return self.tribute

	@staticmethod
	def getPayments(user):
		return Payment.objects.filter(user=user)

	@staticmethod
	def getGain(tributes):
		gain = None
		for tribute in tributes:
			gain = gain + tribute.gain
		return gain

	