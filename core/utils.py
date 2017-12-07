

class Utils:
	@staticmethod
	def validate_value(value):
		str_value = str(value)
		# turn comma to dot
		response = None
		value = str_value.replace(",", ".")
		try:
			value = float(value)
			response = value
		except:
			response = False
		return response

	@staticmethod
	def reverse_date(date):
		"""Reverse dates for portuguese"""
		receive = str.split(str(date), '-')
		return receive[2] + '-' + receive[1] + '-' + receive[0]