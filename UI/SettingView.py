# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: SettingView.py
@createTime: 2020.2.1 21:17
@updateTime: 2020-03-29 20:14:12
"""

import os

import ui
import console

from .AlertView import AlertView
from .TextFileView import TextFileView

from core.AppService import AppService
from core.ConfigService import ConfigService

class SettingDelegate(object):
	def __init__(self,app,father):
		self.app=app
		self.father=father
				
	def tableview_did_select(self,tableview, section, row):

		try:
			if(tableview.data_source.items[row]["title"]=="查看日志"):
				self.app.activity_indicator.start()
				try:
					v=TextFileView("日志",self.app.rootpath+"log.txt")
					if self.app.isIpad():
						v.frame=(0,0,self.father.width+100,self.father.height)
					else:
						v.frame=(0,0,self.father.width,self.father.height)
					v.present("sheet")
					v.wait_modal()
				except Exception as e:
					console.hud_alert('Failed to load TextFileView', 'error', 1.0)
				finally:
					self.app.activity_indicator.stop()
				
		except Exception as e:
			console.hud_alert('Failed to load setting', 'error', 1.0)
		finally:
			pass

class ClaerDelegate(object):
	
	def __init__(self,app,father):
		self.app=app
		self.father=father
				
	def tableview_did_select(self,tableview, section, row):
		
		try:
			if(tableview.data_source.items[row]["title"]=="清除图标"):
				AlertView("清除图标",'你确定要删除所有应用图标吗',self.img_clear_Act)
				
			elif(tableview.data_source.items[row]["title"]=="清除日志"):
				AlertView("清除日志",'你确定要删除日志文件吗',self.log_clear_Act)
			
			elif (tableview.data_source.items[row]["title"]=="初始化系统"):
				AlertView("初始化系统",'你确定要删除所有数据并重置系统吗',self.reset_system_Act)
				
		except Exception as e:
			console.hud_alert('Failed to load clear', 'error', 1.0)
		finally:
			pass
	
	@ui.in_background	
	def img_clear_Act(self):
		self.app.activity_indicator.start()
		try:
			imgs=os.listdir(self.app.rootpath+"img/")
			for i in imgs:
				os.remove(self.app.rootpath+"img/"+i)
			self.father.updateData()
			console.hud_alert('图标清理成功！', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to load AppDetailView', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
	
	@ui.in_background	
	def log_clear_Act(self):
		self.app.activity_indicator.start()
		try:
			if(os.path.exists(self.app.rootpath+"log.txt")):
				os.remove(self.app.rootpath+"log.txt")
			self.father.updateData()
			console.hud_alert('日志清理成功！', 'success', 1.0)
					
		except Exception as e:
			console.hud_alert('Failed to load AppDetailView', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
		
	@ui.in_background
	def reset_system_Act(self):
		self.app.activity_indicator.start()
		try:
			imgs=os.listdir(self.app.rootpath+"img/")
			for i in imgs:
				os.remove(self.app.rootpath+"img/"+i)
				
			if(os.path.exists(self.app.rootpath+"log.txt")):
				os.remove(self.app.rootpath+"log.txt")
				
			self.app.appService.clearDataBase()
			self.app.configService.setDefult()
			self.father.updateData()
			console.hud_alert('系统初始化成功！', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to load AppDetailView', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()

class SettingView (ui.View):
	
	def __init__(self,app,father):
		self.app=app
		self.father=father
		
		self.count_apps=0
		self.count_categorys=0
		self.count_stars=0
		self.count_prices=0
		self.count_totalValue=0
		
		self.cfg_runtimes=0
		self.cfg_notice=1
		self.cfg_downloadimg=1
		self.cfg_log=1
		
		self.datasize_img=0
		self.datasize_log=0
		self.datasize_database=0
		
		self.name="设置"
		self.flex="WHRLTB"
		
		self.fontcolor_pastal="#999999"
		self.fontcolor_deep="#4c4c4c"
		self.fontcolor_warnning="#cf0000"
		
		self.scrollView=ui.ScrollView()
		
		self.count_titleLabel=ui.Label()
		self.count_tableView=ui.TableView()
		self.count_appsLabel=ui.Label()
		self.count_starsLabel=ui.Label()
		self.count_categorysLabel=ui.Label()
		self.count_runtimesLabel=ui.Label()
		self.count_pricesLabel=ui.Label()
		self.count_totalValueLabel=ui.Label()
		
		self.count_tableView.add_subview(self.count_runtimesLabel)
		self.count_tableView.add_subview(self.count_appsLabel)
		self.count_tableView.add_subview(self.count_starsLabel)
		self.count_tableView.add_subview(self.count_categorysLabel)
		self.count_tableView.add_subview(self.count_pricesLabel)
		self.count_tableView.add_subview(self.count_totalValueLabel)
		self.scrollView.add_subview(self.count_titleLabel)
		self.scrollView.add_subview(self.count_tableView)

		self.setting_titleLabel=ui.Label()
		self.setting_tableView=ui.TableView()
		self.settingDelegate=SettingDelegate(self.app,self)
		
		self.setting_noticeBtn=ui.Switch()
		self.setting_downloadBtn=ui.Switch()
		self.setting_logBtn=ui.Switch()
		
		self.setting_tableView.add_subview(self.setting_noticeBtn)
		self.setting_tableView.add_subview(self.setting_downloadBtn)
		self.setting_tableView.add_subview(self.setting_logBtn)
		self.scrollView.add_subview(self.setting_titleLabel)
		self.scrollView.add_subview(self.setting_tableView)
		
		self.clear_titleLabel=ui.Label()
		self.clear_tableView=ui.TableView()
		self.clearDelegate=ClaerDelegate(self.app,self)
		
		self.datasize_imgLabel=ui.Label()
		self.datasize_logLabel=ui.Label()
		self.datasize_sumLabel=ui.Label()
		
		self.clear_tableView.add_subview(self.datasize_imgLabel)
		self.clear_tableView.add_subview(self.datasize_logLabel)
		self.clear_tableView.add_subview(self.datasize_sumLabel)
		self.scrollView.add_subview(self.clear_titleLabel)
		self.scrollView.add_subview(self.clear_tableView)
		
		self.add_subview(self.scrollView)
		
		self.loadData()
		
	def loadData(self):
		
		res=self.app.appService.countApp()
		if(res.isPositive()):
			self.count_apps=res.getData()
			
		res=self.app.appService.countStar()
		if(res.isPositive()):
			self.count_stars=res.getData()
		
		res=self.app.appService.countCategory()
		if(res.isPositive()):
			self.count_categorys=res.getData()
		
		res=self.app.appService.countPrices()
		if(res.isPositive()):
			self.count_prices=res.getData()
			
		res=self.app.appService.sumNewestPrices()
		if(res.isPositive()):
			self.count_totalValue=res.getData()
		
		res=self.app.configService.getRuntimes()
		if(res.isPositive()):
			self.cfg_runtimes=res.getData()
			
		res=self.app.configService.getNotice()
		if(res.isPositive()):
			self.cfg_notice=res.getData()
			
		res=self.app.configService.getDownLoadImg()
		if(res.isPositive()):
			self.cfg_downloadimg=res.getData()
			
		res=self.app.configService.getLog()
		if(res.isPositive()):
			self.cfg_log=res.getData()
			
		imgs=os.listdir(self.app.rootpath+"img/")
		sum=0
		for i in imgs:
			sum+=os.path.getsize(self.app.rootpath+"img/"+i)
		self.datasize_img=sum
		
		if(os.path.exists(self.app.rootpath+"log.txt")):
			self.datasize_log=os.path.getsize(self.app.rootpath+"log.txt")
		else:
			self.datasize_log=0

		if(os.path.exists(self.app.rootpath+"database.db")):
			self.datasize_database=os.path.getsize(self.app.rootpath+"database.db")
		else:
			self.datasize_database=0
			
	def loadUI(self):
		
		"""
		statistic
		------------
		"""
		
		self.count_titleLabel.frame=(20,20,self.width-40,30)
		self.count_titleLabel.text="数据统计"
		self.count_titleLabel.font=("<System>",15)
		self.count_titleLabel.text_color=self.fontcolor_pastal
		
		self.count_runtimesLabel.frame=(self.width-140,10,100,30)
		self.count_runtimesLabel.text=str(self.cfg_runtimes)+"次"
		self.count_runtimesLabel.font=("<System>",18)
		self.count_runtimesLabel.text_color=self.fontcolor_pastal
		self.count_runtimesLabel.alignment=ui.ALIGN_RIGHT
		
		self.count_appsLabel.frame=(self.width-140,60,100,30)
		self.count_appsLabel.text=str(self.count_apps)+"个"
		self.count_appsLabel.font=("<System>",18)
		self.count_appsLabel.text_color=self.fontcolor_pastal
		self.count_appsLabel.alignment=ui.ALIGN_RIGHT
		
		self.count_starsLabel.frame=(self.width-140,110,100,30)
		self.count_starsLabel.text=str(self.count_stars)+"个"
		self.count_starsLabel.font=("<System>",18)
		self.count_starsLabel.text_color=self.fontcolor_pastal
		self.count_starsLabel.alignment=ui.ALIGN_RIGHT
		
		self.count_categorysLabel.frame=(self.width-140,160,100,30)
		self.count_categorysLabel.text=str(self.count_categorys)+"类"
		self.count_categorysLabel.font=("<System>",18)
		self.count_categorysLabel.text_color=self.fontcolor_pastal
		self.count_categorysLabel.alignment=ui.ALIGN_RIGHT
		
		self.count_pricesLabel.frame=(self.width-140,210,100,30)
		self.count_pricesLabel.text=str(self.count_prices)+"条"
		self.count_pricesLabel.font=("<System>",18)
		self.count_pricesLabel.text_color=self.fontcolor_pastal
		self.count_pricesLabel.alignment=ui.ALIGN_RIGHT
		
		self.count_totalValueLabel.frame=(self.width-140,260,100,30)
		self.count_totalValueLabel.text=str(self.count_totalValue)+"  ¥"
		self.count_totalValueLabel.font=("<System>",18)
		self.count_totalValueLabel.text_color=self.fontcolor_pastal
		self.count_totalValueLabel.alignment=ui.ALIGN_RIGHT
		
		count_listdatasource = ui.ListDataSource(
			[
				{"title": "程序运行次数", "accessory_type": "none","image":"typb:Sync"},
				{"title": "App", "accessory_type": "none","image":"typb:Grid"},
				{"title": "愿望单", "accessory_type": "none","image":"typb:Star"},
				{"title": "分类", "accessory_type": "none","image":"typb:Bookmark"},
				{"title": "价格", "accessory_type": "none","image":"typb:Tag"},
				{"title": "应用总价值", "accessory_type": "none","image":"iob:social_bitcoin_256"},
				]
			)
			
		count_listdatasource.delete_enabled = False	
		count_listdatasource.number_of_lines=6
		count_listdatasource.text_color=self.fontcolor_deep
		self.count_tableView.data_source = count_listdatasource
		self.count_tableView.delegate = count_listdatasource
		
		self.count_tableView.row_height=50
		self.count_tableView.frame=(-1,self.count_titleLabel.y+30,self.width+2,count_listdatasource.number_of_lines*self.count_tableView.row_height)
		self.count_tableView.border_width=1
		self.count_tableView.border_color=self.fontcolor_pastal
		self.count_tableView.reload()
		
		"""
		setting
		---------
		"""
		
		self.setting_titleLabel.frame=(20,self.count_tableView.y+self.count_tableView.height+40,self.width-40,30)
		self.setting_titleLabel.text="设置选项"
		self.setting_titleLabel.font=("<System>",15)
		self.setting_titleLabel.text_color=self.fontcolor_pastal
		
		setting_listdatasource = ui.ListDataSource(
			[
				{"title": "降价通知（愿望单中的App）", "accessory_type": "none","image":"typb:Unmute"},
				{"title": "图标下载", "accessory_type": "none","image":"iob:images_256"},
				{"title": "记录日志", "accessory_type": "none","image":"typb:Write"},
				{"title": "查看日志", "accessory_type": "disclosure_indicator","image":"typb:Calendar"},
				]
			)
			
		setting_listdatasource.delete_enabled = False	
		setting_listdatasource.number_of_lines=4
		setting_listdatasource.text_color=self.fontcolor_deep
		self.setting_tableView.data_source = setting_listdatasource
		self.setting_tableView.delegate = self.settingDelegate
		
		self.setting_noticeBtn.frame=(self.width-70,10,100,30)
		self.setting_noticeBtn.tint_color="#0987b4"
		self.setting_noticeBtn.value=self.cfg_notice
		self.setting_noticeBtn.action=self.notice_st_Act
		
		self.setting_downloadBtn.frame=(self.width-70,60,100,30)
		self.setting_downloadBtn.tint_color="#0987b4"
		self.setting_downloadBtn.value=self.cfg_downloadimg
		self.setting_downloadBtn.action=self.download_st_Act
		
		self.setting_logBtn.frame=(self.width-70,110,100,30)
		self.setting_logBtn.tint_color="#0987b4"
		self.setting_logBtn.value=self.cfg_log
		self.setting_logBtn.action=self.log_st_Act
		
		self.setting_tableView.row_height=50
		self.setting_tableView.frame=(-1,self.setting_titleLabel.y+30,self.width+2,setting_listdatasource.number_of_lines*self.setting_tableView.row_height)
		self.setting_tableView.border_width=1
		self.setting_tableView.border_color=self.fontcolor_pastal
		self.setting_tableView.reload()
		
		"""
		cleardata
		--------
		"""
		
		self.clear_titleLabel.frame=(20,self.setting_tableView.y+self.setting_tableView.height+40,self.width-40,30)
		self.clear_titleLabel.text="数据清理"
		self.clear_titleLabel.font=("<System>",15)
		self.clear_titleLabel.text_color=self.fontcolor_pastal
		
		self.datasize_imgLabel.frame=(self.width-140,10,100,30)
		self.datasize_imgLabel.text="{f:.2f}".format(f=(self.datasize_img/1024/1024))+"MB"
		self.datasize_imgLabel.font=("<System>",18)
		self.datasize_imgLabel.text_color=self.fontcolor_pastal
		self.datasize_imgLabel.alignment=ui.ALIGN_RIGHT
		
		self.datasize_logLabel.frame=(self.width-140,60,100,30)
		self.datasize_logLabel.text="{f:.2f}".format(f=(self.datasize_log/1024/1024))+"MB"
		self.datasize_logLabel.font=("<System>",18)
		self.datasize_logLabel.text_color=self.fontcolor_pastal
		self.datasize_logLabel.alignment=ui.ALIGN_RIGHT
		
		self.datasize_sumLabel.frame=(self.width-140,110,100,30)
		self.datasize_sumLabel.text="{f:.2f}".format(f=(self.datasize_img+self.datasize_log+self.datasize_database)/1024/1024)+"MB"
		self.datasize_sumLabel.font=("<System>",18)
		self.datasize_sumLabel.text_color=self.fontcolor_pastal
		self.datasize_sumLabel.alignment=ui.ALIGN_RIGHT
		
		clear_listdatasource = ui.ListDataSource(
			[
				{"title": "清除图标", "accessory_type": "disclosure_indicator","image":"typb:Trash"},
				{"title": "清除日志", "accessory_type": "disclosure_indicator","image":"typb:Trash"},
				{"title": "初始化系统", "accessory_type": "disclosure_indicator","image":"typb:Refresh"},
				]
			)
			
		clear_listdatasource.delete_enabled = False	
		clear_listdatasource.number_of_lines=3
		clear_listdatasource.text_color=self.fontcolor_warnning
		self.clear_tableView.data_source = clear_listdatasource
		self.clear_tableView.delegate = self.clearDelegate
		
		self.clear_tableView.row_height=50
		self.clear_tableView.frame=(-1,self.clear_titleLabel.y+30,self.width+2,clear_listdatasource.number_of_lines*self.clear_tableView.row_height)
		self.clear_tableView.border_width=1
		self.clear_tableView.border_color=self.fontcolor_pastal
		self.clear_tableView.reload()
		
		
		self.scrollView.frame=(0,0,self.width,self.height)
		self.scrollView.content_size=(self.width,self.clear_tableView.y+self.clear_tableView.height+60)
		self.scrollView.background_color="#fafafa"
		
	def layout(self):
		self.loadUI()
		
	def updateData(self):
		self.loadData()	
		self.loadUI()
		
	def notice_st_Act(self,sender):
		v=self.setting_noticeBtn.value
		self.app.configService.setNotice(v)
		
	def download_st_Act(self,sender):
		v=self.setting_downloadBtn.value
		self.app.configService.setDownLoadImg(v)
		
	def log_st_Act(self,sender):
		v=self.setting_logBtn.value
		
		if(v==1):
			self.app.configService.setLogger_Run(v)
			self.app.appService.setLogger_Run(v)
			self.app.configService.setLog(v)
		else:
			self.app.configService.setLog(v)
			self.app.configService.setLogger_Run(v)
			self.app.appService.setLogger_Run(v)
		
	
if __name__ == "__main__":
	v=SettingView(None,None)
	v.frame=(0,0,550,600)
	v.present("sheet")
