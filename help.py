import tkinter as tk
import time
import csv
import sqlite3
from turtle import update

class Helping:
    def __init__(self):
        self.out = ''

        self.root = tk.Tk()
        self.root.title('互帮互助')

        self.conn = sqlite3.connect('helping.db')
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists helping (name text not null, quantity integer);')
        
        self.lb_item = tk.Label(self.root,text='请输入物品名',fg='black',bg='white')
        self.lb_item.grid(row=0,column=0,columnspan=2)  
        self.entry_item = tk.Entry(self.root)
        self.entry_item.grid(row=1,column=0,columnspan=2)
        self.lb_number = tk.Label(self.root,text='物品数量',fg='black',bg='white')
        self.lb_number.grid(row=0,column=3,columnspan=1) 
        self.entry_number = tk.Entry(self.root)
        self.entry_number.grid(row=1,column=3,columnspan=1)

        self.lb_putout = tk.Label(self.root,text=self.out,fg='black',bg='white')
        self.lb_putout.grid(row=3,column=0,columnspan=4)  

        self.bn_add = tk.Button(self.root,text='添加',command=self.on)
        self.bn_add.grid(row=2,column=0,columnspan=1)

        self.bn_delete = tk.Button(self.root,text='删除',command=self.off)
        self.bn_delete.grid(row=2,column=1,columnspan=1)       

        self.bn_search = tk.Button(self.root,text='搜索',command=self.find)
        self.bn_search.grid(row=2,column=2,columnspan=1)
        
        self.bn_list = tk.Button(self.root,text='显示物品列表',command=self.lst)
        self.bn_list.grid(row=2,column=3,columnspan=1)      

        self.root.mainloop()

    def on(self):
        it = self.entry_item.get()
        num = self.entry_number.get()
        if it == '':
            self.out = '请输入物品名'
        else:
            if num == '':
                self.out = '请输入物品数量'
            else:
                if num.isdigit():
                    self.cur.execute('select * from helping where name like "%s"'  %it)
                    if self.cur.fetchone() is None:
                        self.cur.execute('insert into helping values("%s","%s")' %(it,num))
                        self.conn.commit()
                    else:
                        #print(type(self.cur.fetchone()))
                        it_ = self.cur.fetchone()
                        num = str(int(it_[1]) + int(num))
                        self.cur.execute('update helping set quantity="%s" where name="%s"' %(it,num))
                        self.conn.commit()
                        
                else:
                    self.out = '物品数量应为正整数'
                           
    def off(self):
        it = self.entry_item.get()
        num = self.entry_number.get()
        if it == '':
            self.out = '请输入物品名'
        else:
            if num == '':
                self.out = '请输入物品数量'
            else:
                if num.isdigit():
                    self.cur.execute('select * from helping where name like "%s"'  %it)
                    if self.cur.fetchone() is None:
                        self.out = '物品不存在'  
                    else:
                        it_ = self.cur.fetchone() 
                        if str(num) > str(it_[1]):
                            self.out = '物品数目不足'
                        elif str(num) == str(it_[1]):
                            self.cur.execute('delete from helping where name = "%s" limit 1' %it)
                            self.conn.commit()
                        else:
                            num = str(int(it_[1]) - int(num))
                            self.cur.execute('update helping set quantity="%s" where name="%s"' %(it,num))
                            self.conn.commit() 
                else:
                    self.out = '物品数量应为正整数'
                 

    def find(self):
        it = self.entry_item.get()
        if it == '':
            self.out = '请输入物品名'
        else:
            self.cur.execute('select * from helping where name like "%%%s%%"' % it)
            for record in self.cur.fetchall():self.out = self.out + record + '\n' 
            

    def lst(self):
        self.cur.execute('select * from helping')
        for record in self.cur.fetchall():self.out = self.out + record + '\n' 

Helping = Helping()

