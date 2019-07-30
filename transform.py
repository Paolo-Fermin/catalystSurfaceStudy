from paraview.simple import *
import os

velocity = 1

fields = ['delT', 'Uz', 'nut']

print(fields)

time_range = 1
while os.path.exists(os.path.join(os.getcwd(),'insitu', fields[2] + '_%d.vtm'%time_range)):
	time_range += 1

print(time_range)	#note that time range is 1 above the real value
for time in range(1,time_range):
	for field in fields:
		print('Reading field %s for timestep %d' % (field, time))
		reader = XMLMultiBlockDataReader(FileName=os.path.join(os.getcwd(),'insitu', field + '_%d.vtm'%time))
		transform = Transform(Input=reader)
		transform.Transform = 'Transform'
		transform.Transform.Translate = [velocity * time, 0, 0]
		
		writer = servermanager.writers.XMLMultiBlockDataWriter(Input=transform, FileName=os.path.join(os.getcwd(),'transforms',field,field + 'transform_%d.vtm'%time))

		writer.UpdatePipeline()
