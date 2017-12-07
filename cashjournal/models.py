from django.db import models
from accounts.models import User


class Launch(models.Model):
	TYPE_LAUNCH = (
		('en', 'Entrada'),
		('ex', 'Saída'),
	)

	from datetime import date
	date = models.DateField(default=date.today, editable=False)
	description = models.CharField('Descrição', max_length=50,
		help_text="No máximo 50 caractéres")
	value = models.DecimalField('Valor R$', max_digits=5,
		decimal_places=2,
		help_text='Por favor, use ponto em vez de vírgula')
	l_type = models.CharField('Tipo', max_length=2,
		choices=TYPE_LAUNCH)
	user = models.ForeignKey(User,
		on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.description

	@staticmethod
	def getLaunches(user):
		return Launch.objects.filter(user=user)

	@staticmethod
	def statisticData(launches):
		"""get infos in that launchs"""
		n_entries = 0
		n_exits = 0
		amount_entries = 0
		amount_exits = 0
		list_entries = []
		list_exits = []

		for launch in launches:
			if launch.l_type == 'en':
				n_entries = n_entries + 1
				amount_entries = amount_entries + launch.value
			else:
				n_exits = n_exits + 1
				amount_exits = amount_exits + launch.value

		return (n_entries, n_exits, amount_entries, amount_exits)

	def editLaunch(data):
		sql = """update cashjournal_launch set description = '{}', 
		value = {} where id = {}""".format(data['description'], 
			data['value'], data['launch_id'])
		try:
			from django.db import connection
			cursor = connection.cursor()
			cursor.execute(sql)
			return True
		except Exception as e:
			return False
		

class Entrie(Launch):
	TYPE_ENTRIE = (
		('mo', 'Dinheiro'),
		('ch', 'Cheque'),
		('de', 'Débito'),
		('cr', 'Crédito'),
		('tr', 'Transferência'),
		('dp', 'Depósito'),
		('ot', 'Outro')
	)

	en_type = models.CharField('Tipo', max_length=2,
		choices=TYPE_ENTRIE)

	@staticmethod
	def getForLaunchId(launch_id):
		sql = """select * from cashjournal_entrie 
		where launch_ptr_id = {}""".format(launch_id)
		entries = Entrie.objects.raw(sql)
		return entries[0]

	@staticmethod
	def editType(launch_id, en_type):
		sql = """select * from cashjournal_entrie 
		where launch_ptr_id = {}""".format(launch_id)
		entrie = Entrie.objects.raw(sql)[0]
		sql = """
			update cashjournal_entrie 
			set en_type='{}' 
			where launch_ptr_id={} 
			""".format(en_type, launch_id)
		if entrie.en_type != en_type:
			try:
				from django.db import connection
				cursor = connection.cursor()
				cursor.execute(sql)
				return True 
			except Exception:
				return False
		else:
			return True



	

class Exit(Launch):
	TYPE_EXIT = (
		('pa', 'Pagamento'),
		('cw', 'Retirada'),
	)

	ex_type = models.CharField('Tipo', max_length=2,
		choices=TYPE_EXIT)

	@staticmethod
	def getForLaunchId(launch_id):
		sql = """select * from cashjournal_exit 
		where launch_ptr_id = {}""".format(launch_id)
		exits = Exit.objects.raw(sql)
		return exits[0]

	@staticmethod
	def editType(launch_id, ex_type):
		sql = """select * from cashjournal_exit 
		where launch_ptr_id = {}""".format(launch_id)
		exit = Exit.objects.raw(sql)[0]
		sql = """
			update cashjournal_exit 
			set ex_type='{}' 
			where launch_ptr_id={} 
			""".format(ex_type, launch_id)
		if exit.ex_type != ex_type:
			try:
				from django.db import connection
				cursor = connection.cursor()
				cursor.execute(sql)
				return True 
			except Exception:
				return False
		else:
			return True
	 
