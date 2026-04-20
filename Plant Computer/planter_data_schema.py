import struct
class PlanterToPC:
	data_length = 48
	struct_format = "<f????????fffffffff"
	time: float
	vlv0: bool
	vlv1: bool
	vlv2: bool
	vlv3: bool
	vlv4: bool
	vlv5: bool
	light0: bool
	light1: bool
	sns0: float
	sns1: float
	sns2: float
	sns3: float
	sns4: float
	sns5: float
	sns6: float
	sns7: float
	real_time: float
	def unpack_values(self, data: bytes):
		assert len(data) == self.data_length
		unpacked_values = struct.unpack(self.struct_format, data)
		self.time = float(unpacked_values[0])
		self.vlv0 = bool(unpacked_values[1])
		self.vlv1 = bool(unpacked_values[2])
		self.vlv2 = bool(unpacked_values[3])
		self.vlv3 = bool(unpacked_values[4])
		self.vlv4 = bool(unpacked_values[5])
		self.vlv5 = bool(unpacked_values[6])
		self.light0 = bool(unpacked_values[7])
		self.light1 = bool(unpacked_values[8])
		self.sns0 = float(unpacked_values[9])
		self.sns1 = float(unpacked_values[10])
		self.sns2 = float(unpacked_values[11])
		self.sns3 = float(unpacked_values[12])
		self.sns4 = float(unpacked_values[13])
		self.sns5 = float(unpacked_values[14])
		self.sns6 = float(unpacked_values[15])
		self.sns7 = float(unpacked_values[16])
		self.real_time = float(unpacked_values[17])
	def make_header(self) -> str:
		return "time, vlv0, vlv1, vlv2, vlv3, vlv4, vlv5, light0, light1, sns0, sns1, sns2, sns3, sns4, sns5, sns6, sns7, real_time, \n"
	def make_csv_line(self) -> str:
		return f"{self.time},{self.vlv0},{self.vlv1},{self.vlv2},{self.vlv3},{self.vlv4},{self.vlv5},{self.light0},{self.light1},{self.sns0},{self.sns1},{self.sns2},{self.sns3},{self.sns4},{self.sns5},{self.sns6},{self.sns7},{self.real_time},\n"
