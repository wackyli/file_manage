#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 
# Title:File Manage 本地文件管理脚本
# author :wackl
# 
# github : https://github.com/wackyli/
# 
'''
注意：当前脚本只对单盘分区内文件进行整理
使用watchdog中FileSystemEventHandler下on_modified函数
'''

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#pip install watchdog

import os 
import time
from time import strftime
from datetime import datetime


# 自定义归档目标文件夹/文件夹命
# to_folder_name = 'tohere'
folder_to_track = "C:/Users/lifei/Desktop/in"
folder_destination = "C:/Users/lifei/Desktop/tohere"
to_folder_name = folder_destination.split('/')[-1]

class myhandler(FileSystemEventHandler):
	def on_modified(self,event):
		for filename in os.listdir(folder_to_track):
			i = 1
			if filename != to_folder_name:
				new_name = filename
				extension = 'noname'
				try:
					extension = str(os.path.splitext(folder_to_track+'/'+filename)[1])
					path = extension_folders[extension]
				except:
					extension = 'noname'

				#时间
				now = datetime.now()
				year = now.strftime('%Y')
				month = now.strftime('%m')
				day = now.strftime('%d')
				minsec = now.strftime('%M%S')

				#定义路径
				folder_destination_path = extension_folders[extension]

				year_exist = False
				month_exist = False

				#判断路径地址是否存在并建立
				folder_exist = os.path.exists(extension_folders[extension])

				if not folder_exist:
					os.mkdir(extension_folders[extension])
					folder_destination_path = extension_folders[extension]

				#处理以时间划分文件夹
				for folder_name in os.listdir(extension_folders[extension]):
					if folder_name == year:
						folder_destination_path = extension_folders[extension]+'/'+year
						year_exist = True

						for folder_month in os.listdir(folder_destination_path):
							if month == folder_month:
								folder_destination_path = extension_folders[extension] +'/'+year+'/'+month
								month_exist = True

				#判断时间结构文件夹并建立
				if not year_exist:
					os.mkdir(extension_folders[extension] + '/' + year)
					folder_destination_path = extension_folders[extension] + '/' + year

				if not month_exist:
					os.mkdir(folder_destination_path + '/' + month)
					folder_destination_path = folder_destination_path + '/' + month

				#重复文件处理
				file_exists = os.path.isfile(folder_destination_path + '/' + new_name)
				while file_exists:
					i += 1
					new_name = os.path.splitext(folder_to_track + '/' + filename)[0] + '_'+str(i) + ('_{y}{m}{d}_{ms}').format(y=year[-2:],m=month,d=day,ms=minsec) + os.path.splitext(folder_to_track + '/' + filename)[1]
					new_name = new_name.split('/')[-1]

					file_exists = os.path.isfile(folder_destination_path+'/'+new_name)
					# print('重复文件：',(folder_destination_path+'/'+new_name))

				src = folder_to_track + '/' + filename
				new_name = folder_destination_path + '/'+ new_name

				os.rename(src,new_name)


extension_folders = {
	# 没有文件后缀
	'noname':folder_destination +'/'+'noname',

	# 图片
	'.jpg': folder_destination + '/' +'Image',
	'.jpeg': folder_destination + '/' +'Image',
	'.png': folder_destination + '/' +'Image',
	'.gif': folder_destination + '/' +'Image',
	'.bmp': folder_destination + '/' +'Image',
	'.tif': folder_destination + '/' +'Image',
	'.tiff': folder_destination + '/' +'Image',
	'.CR2': folder_destination + '/' +'Image',

	# 文本格式
	'.txt':folder_destination + '/' +'txtfolder',
	'.pdf':folder_destination + '/' +'txtfolder',
	'.doc':folder_destination + '/' +'txtfolder',
	'.docx':folder_destination + '/' +'txtfolder',
	'.odt':folder_destination + '/' +'txtfolder',
	'.rtf':folder_destination + '/' +'txtfolder',
	'.tex':folder_destination + '/' +'txtfolder',
	'.wps':folder_destination + '/' +'txtfolder',
	'.wks':folder_destination + '/' +'txtfolder',
	'.wpd':folder_destination + '/' +'txtfolder',
	'.ppt':folder_destination + '/' +'txtfolder',
	'.pptx':folder_destination + '/' +'txtfolder',

	# 数据文件
	'.xls':folder_destination + '/' +'database',
	'.xlsx':folder_destination + '/' +'database',	
	'.csv':folder_destination + '/' +'database',
	'.json':folder_destination + '/' +'database',
	'.sql':folder_destination + '/' +'database',
	'.xml':folder_destination + '/' +'database',
	'.mdb':folder_destination + '/' +'database',
	'.tar':folder_destination + '/' +'database',

	# 编程语言
	'.py': folder_destination + '/' +'Python',
	'.class': folder_destination + '/' +'Java',
	'.c': folder_destination + '/' +'C&C++',

	# 安装文件
	'.exe': folder_destination + '/' +'executable',
	'.apk': folder_destination + '/' +'executable',
	'.jar': folder_destination + '/' +'executable',

	# 压缩文件
	'.zip': folder_destination + '/' +'Compressed',
	'.rar': folder_destination + '/' +'Compressed',
	'.rar': folder_destination + '/' +'Compressed',
	'.7z': folder_destination + '/' +'Compressed',
	'.z': folder_destination + '/' +'Compressed',
	'.tar.gz': folder_destination + '/' +'Compressed',
	'.pkg': folder_destination + '/' +'Compressed',

	# 视频
	'.mp4': folder_destination + '/' +'Video',
	'.avi': folder_destination + '/' +'Video',
	'.vob': folder_destination + '/' +'Video',
	'.mov': folder_destination + '/' +'Video',
	# music
	'.mp3':folder_destination + '/' +'music',
	'.wav':folder_destination + '/' +'music',
	'.ogg':folder_destination + '/' +'music',
	'.mp3':folder_destination + '/' +'music',
	'.aif':folder_destination + '/' +'music',
	'.mid':folder_destination + '/' +'music'
}


if __name__ == '__main__':
	event_handler = myhandler()
	observer = Observer()
	observer.schedule(event_handler,folder_to_track,recursive=True)
	observer.start()

	try:
		while True:
			time.sleep(10)

	except KeyboardInterrupt:
		observer.stop()

	observer.join()

