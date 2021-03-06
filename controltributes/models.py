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

	@staticmethod
	def editTribute(data, tribute_id):
		update = False
		try:
			tribute = Tribute.objects.get(id=tribute_id)
			
			if tribute.description != data['description']:
				tribute.description = data['description']
				update = True
				
			if tribute.period != data['period']:
				tribute.period = data['period']
				update = True
			
			if update:
				tribute.save()
				return "Tributo alterado com sucesso!"
			else:
				return "Nenhuma alteração foi detectada"

		except Exception as e:
			print(e)
			return False

	@staticmethod
	def getDescription(tribute_id):
		tribute = Tribute.objects.get(id=tribute_id)
		return tribute.description

	@staticmethod
	def getTributesForPeriod(user_id, init_date, end_date):
		tributes = Tribute.getTributes(user_id)
		list_payments_for_tributes = []
		amount = 0
		n_payments = 0
		for t in tributes:
			payments = Payment.getPaymentsForPeriod(t.id, init_date, end_date)
			for p in payments:
				list_payments_for_tributes.append((t.description, t.period, p.date, p.value))
				amount += p.value
				n_payments += 1
				
		return list_payments_for_tributes, amount, n_payments


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

	@staticmethod
	def getPaymentsForTributes(user_id):
		tributes = Tribute.getTributes(user_id=user_id)
		payments_list = []
		for tribute in tributes:
			payments = Payment.objects.filter(tribute_id=tribute.id)
			if payments:
				for payment in payments:
					payments_list.append((tribute.id, tribute.period, tribute.description, 
						payment.date, payment.value, payment.id))
		return payments_list

	@staticmethod
	def getPaymentsRelateds(tribute_id):
		payments = Payment.objects.filter(tribute_id=tribute_id)
		tribute_description = Tribute.getDescription(tribute_id)
		sum_payments = 0
		for payment in payments:
			sum_payments = sum_payments + payment.value
		return payments, sum_payments, tribute_description
	
	def getPaymentsForPeriod(tribute_id, init_date, end_date):
		sql = """
			SELECT * from controltributes_payment 
			WHERE tribute_id = {}
			AND date >= '{}' And date <= '{}';
		""".format(tribute_id, init_date, end_date)
		return Payment.objects.raw(sql)

	

	