#define BUFFER_SIZE 48
class PlanterToPC
{
public:
	float time;
	_Bool vlv0;
	_Bool vlv1;
	_Bool vlv2;
	_Bool vlv3;
	_Bool vlv4;
	_Bool vlv5;
	_Bool light0;
	_Bool light1;
	float sns0;
	float sns1;
	float sns2;
	float sns3;
	float sns4;
	float sns5;
	float sns6;
	float sns7;
	float real_time;
	int size = BUFFER_SIZE;
	char buffer[BUFFER_SIZE];

	char *make_data_buffer()
	{
		memcpy(&buffer[0], &time, 4);
		memcpy(&buffer[4], &vlv0, 1);
		memcpy(&buffer[5], &vlv1, 1);
		memcpy(&buffer[6], &vlv2, 1);
		memcpy(&buffer[7], &vlv3, 1);
		memcpy(&buffer[8], &vlv4, 1);
		memcpy(&buffer[9], &vlv5, 1);
		memcpy(&buffer[10], &light0, 1);
		memcpy(&buffer[11], &light1, 1);
		memcpy(&buffer[12], &sns0, 4);
		memcpy(&buffer[16], &sns1, 4);
		memcpy(&buffer[20], &sns2, 4);
		memcpy(&buffer[24], &sns3, 4);
		memcpy(&buffer[28], &sns4, 4);
		memcpy(&buffer[32], &sns5, 4);
		memcpy(&buffer[36], &sns6, 4);
		memcpy(&buffer[40], &sns7, 4);
		memcpy(&buffer[44], &real_time, 4);
		return buffer;
	};
};