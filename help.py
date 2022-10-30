        import tkinter as tk
import sqlite3

class Helping:
    def __init__(self):
        self.out = '^-^'

        self.root = tk.Tk()
        self.root.title('互帮互助')

        self.conn = sqlite3.connect('helping.db')
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists helping (name text not null, quantity text);')
        
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

    #添加物品
    def on(self):
        it = self.entry_item.get()
        num = self.entry_number.get()
        if it == '':
            self.lb_putout.config(text= '请输入物品名') 
        else:
            if num == '':
                self.lb_putout.config(text='请输入物品数量')
            else:
                if num.isdigit():
                    self.cur.execute('select * from helping where name like "%s"'  %it)
                    if (fetch :=self.cur.fetchone()) is None:
                        self.cur.execute('insert into helping values("%s","%s")' %(it,num))
                        self.conn.commit()
                        self.lb_putout.config(text = '输入成功')
                    else:
                        #print(type(self.cur.fetchone()))
                        num = str(int(fetch[1]) + int(num))
                        self.cur.execute('update helping set quantity="%s" where name="%s"' %(num,it))
                        self.conn.commit()
                        self.lb_putout.config(text = '输入成功')
                        
                else:
                    self.lb_putout.config(text= '物品数量应为正整数')

    #删除物品                           
    def off(self):
        it = self.entry_item.get()
        num = self.entry_number.get()
        if it == '':
            self.lb_putout.config(text='请输入物品名')
        else:
            if num == '':
                self.lb_putout.config(text = '请输入物品数量')
            else:
                if num.isdigit():
                    self.cur.execute('select * from helping where name like "%s"'  %it)
                    if (fetch:=self.cur.fetchone()) is None:
                        self.lb_putout.config(text = '物品不存在')
                    else:
                        if str(num) > str(fetch[1]):
                            self.lb_putout.config(text = '物品数目不足')
                        elif str(num) == str(fetch[1]):
                            self.cur.execute('delete from helping where name = "%s" ' %it)
                            self.conn.commit()
                            self.lb_putout.config(text = '删除成功')
                        else:
                            num = str(int(fetch[1]) - int(num))
                            self.cur.execute('update helping set quantity="%s" where name="%s"' %(num,it))
                            self.conn.commit() 
                            self.lb_putout.config(text = '删除成功')
                else:
                    self.lb_putout.config(text = '物品数量应为正整数')
                 
    #查找物品
    def find(self):
        it = self.entry_item.get()
        if it == '':
            self.lb_putout.config(text = '请输入物品名')
        else:
            self.out=''
            self.cur.execute('select * from helping where name like "%%%s%%"' %it)
            for record in self.cur.fetchall():self.out = self.out + str(record) + '\n' 
            self.lb_putout.config(text=self.out)            

    #显示物品清单
    def lst(self):
        self.out = ''
        self.cur.execute('select * from helping')
        for record in self.cur.fetchall():self.out = self.out + str(record) + '\n' 
        self.lb_putout.config(text=self.out)

Helping = Helping()

