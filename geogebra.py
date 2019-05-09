from tkinter import *

import numpy
from tkinter.font import Font
import math
import time
import threading
alphabet = [chr(i) for i in range(ord('a'),ord('z')+1)]


from PIL import ImageTk, Image
import os


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t




import random

def random_color():
    return random.randint(0,0x1000000)



root =  Tk()
root.title("Geogebra revisité")





width, height = 1920, 1080;
leftFrame =  Frame(root,     borderwidth="0", relief="flat" )
leftFrame_text =  Frame(leftFrame, borderwidth="3", relief="flat" )
leftFrame_input =  Frame(leftFrame, borderwidth="3", relief="flat")

rightFrame =  Frame(root, borderwidth="3", relief="flat" )
rightFrame_top =  Frame(rightFrame, borderwidth="3", relief="flat" )
rightFrame_bot =  Frame(rightFrame, borderwidth="3", relief="flat" )


leftFrame.grid(column=0, row=0, sticky="ns" )
leftFrame_text.grid(column=0, row=1, sticky="ns")
leftFrame_input.grid(column=0, row=0, sticky="ns")




# --- create canvas with scrollbar ---

canvas =  Canvas(leftFrame_text, height=900, width=250)
canvas.pack(side= LEFT, fill=BOTH)

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))


xscrollbar = Scrollbar(leftFrame_text, orient=HORIZONTAL, command=canvas.xview)
xscrollbar.pack(side=BOTTOM, fill=X)
yscrollbar = Scrollbar(leftFrame_text, orient=VERTICAL, command=canvas.yview)
yscrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(xscrollcommand= xscrollbar.set)
canvas.configure(yscrollcommand= yscrollbar.set)



# update scrollregion after starting 'mainloop'
# when all widgets are in canvas
canvas.bind('<Configure>', on_configure)


# --- put frame in canvas ---

frame =  Frame(canvas)
canvas.create_window((0,0), window=frame, anchor='nw', height=40000, width=500)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

rightFrame.grid(column=1, row=0)
rightFrame_top.grid(column=0, row=0)
rightFrame_bot.grid(column=0, row=1)
rightFrame_bot.config(height=40)

load_pointImg = Image.open("point.png")
load_pointImg=load_pointImg.resize((25, 25) )
pointImg = ImageTk.PhotoImage(load_pointImg)




def entryReturn(arg=None):
    result = entry.get()
    if (result[0:5]=="f(x)="):
        color = '{:06x}'.format(random_color())

        a = result[5:len(result)] # len("f(x)=") = 5 btw


        f = Function( alphabet[len(graph.functions)%26], a, ('#'+ color))
        graph.functions.append(f);
        graph.show();
        f.showLeftLabel();






entry = Entry(leftFrame_input);
entry.pack();
entry.bind("<Return>", entryReturn)


'''
btn = Button(rightFrame_top, text="Point" );
btn.grid(column=0, row=0);
btn = Button(rightFrame_top, text="Cercle");
btn.grid(column=1, row=0);
'''


w = Canvas(rightFrame_bot, width=width, height=height, background='#FFFFFF' )
w.pack()
angle= [0, 0, 0];

projection = [
    [1, 0, 0],
    [0, 1, 0],
];



class Variable:
	def __init__(self ):
		self.name = "Var_" + str(alphabet[len(graph.variables)%26]);
		self.value = 0; # float
		self.l = LeftFrameLabel("Variable " + self.name);

	def delete(self, event):
		del graph.variables[graph.variables.index(self)]
		self.l._img.grid_forget();
		self.l.label.grid_forget();
		self.l.quitLabel.grid_forget();
		graph.show();

	def variablePreference(self):
		def apply_button():
			self.value = float(self.numberScale.get())
			self.l.label.config(text= "Variable " + self.name + " = " + str(self.value) );
			graph.show();

		def variate_apply():
			self.value += self.resolutionNumber;
			self.l.label.config(text= "Variable " + self.name + " = " + str(self.value) );
			graph.showFunctions();

		def frange(x, y, jump):
			while x < y:
				yield x
				x += jump

		def variate_button():
			self.fromNumber = float(self.fromEntry.get());
			self.toNumber = float(self.toEntry.get());
			self.resolutionNumber = float(self.resolutionEntry.get());
			self.value = self.fromNumber;
			#while (self.value <= toNumber):
			generator = frange(self.fromNumber, self.toNumber, self.resolutionNumber);

			loopT=0;
			for i in generator:
				loopT+=1;
				threading.Timer(loopT, variate_apply).start()


		self.preference_root =  Toplevel(root)

		self.valueLabel = Label(self.preference_root, text="Value")
		self.valueLabel.pack(fill=BOTH, expand=TRUE);

		self.numberScale = Scale(self.preference_root, from_=-1000, to=1000,  resolution=0.1, orient=HORIZONTAL)
		self.numberScale.pack(fill=BOTH, expand=TRUE);

		self.applyButton = Button(self.preference_root, text="Apply", command=apply_button);
		self.applyButton.pack(fill=BOTH, expand=TRUE);

		self.frame_ =  Frame(self.preference_root, borderwidth="3", relief="flat" )

		self.runButton = Button(self.frame_, text="Variate", command=variate_button);
		self.runButton.grid(row=0, column=0);

		self.fromEntry = Entry(self.frame_ );
		self.fromEntry.grid(row=0, column=1);
		self.fromEntry.insert(0, 'From')

		self.toEntry = Entry(self.frame_ );
		self.toEntry.grid(row=0, column=2);
		self.toEntry.insert(0, 'To')

		self.resolutionEntry = Entry(self.frame_ );
		self.resolutionEntry.grid(row=0, column=3);
		self.resolutionEntry.insert(0, 'Resolution')

		self.frame_.pack(fill=BOTH, expand=TRUE)




	def showLeftLabel(self):
		self.l.text = "Variable " + self.name + " = " + str(self.value)
		self.l.show();
		self.l.quitLabel.bind("<Button-1>", self.delete)
		self.l.label.config(command=self.variablePreference)





class LeftFrameLabel:
	def __init__(self, text):
		self.text=text;

	def show(self):
		row=len(graph.points)+len(graph.functions)+len(graph.polygons)+len(graph.variables);

		self._img = Label(frame, image=pointImg )
		self._img.grid(row=row, column=2)

		self.label = Button(frame, text=self.text, font=(None, 9))
		self.label.config(relief="flat", foreground="#000000", background="#e0e0e0", anchor="w")
		self.label.grid(row=row, column=1);

		self.quitLabel = Button(frame, text="X", foreground="red", relief="flat")
		self.quitLabel.grid(row=row, column=0);



class Polygon:
	def __init__(self, points):
		self.points = points;
		self.l = LeftFrameLabel("Polygon " + str(alphabet[len(graph.polygons)%26]));

	def show(self):
		lastX="nan";
		lastY="nan";
		firstX="nan";
		firstY="nan";
		#self.points[i].show();
		rotationZ = [
			[math.cos(angle[2]), -math.sin(angle[2]), 0],
			[math.sin(angle[2]), math.cos(angle[2]), 0],
			[0, 0, 1],
		];

		rotationX = [
			[1, 0, 0],
			[0, math.cos(angle[0]), -math.sin(angle[0])],
			[0, math.sin(angle[0]), math.cos(angle[0])],
		];

		rotationY = [
			[math.cos(angle[1]), 0, math.sin(angle[1])],
			[0, 1, 0],
			[-math.sin(angle[1]), 0, math.cos(angle[1])],
		];


		for i in range(len(self.points)):
			projected=[];
			rotated = numpy.dot(rotationY, [self.points[i].graph_posX, self.points[i].graph_posY, self.points[i].posZ]);
			rotated = numpy.dot(rotationX, rotated);
			rotated = numpy.dot(rotationZ, rotated);
			projected2d = numpy.dot(projection, rotated);
			
			real_posX = graphToReal(projected2d[0], projected2d[1])[0];
			real_posY = graphToReal(projected2d[0], projected2d[1])[1];
			#real_posX = graphToReal(self.points[i].graph_posX, self.points[i].graph_posY)[0]
			#real_posY = graphToReal(self.points[i].graph_posX, self.points[i].graph_posY)[1]
			if (lastX is not "nan" and lastY is not "nan"):
				w.create_line(lastX, lastY, real_posX, real_posY, width=2, fill="IndianRed1");
			if (i==0):
				firstX=real_posX;
				firstY=real_posY;
				
			lastX=real_posX;
			lastY=real_posY;
			if (i> 1 and i != len(self.points)-1):
				w.create_line(real_posX, real_posY, firstX, firstY , dash=(4, 2), width=2, fill="IndianRed4");
			
		w.create_line(lastX, lastY, firstX, firstY, width=2, fill="IndianRed1");

		#w.create_line(lastX, lastY, graphToReal(self.points[0].graph_posX, self.points[0].graph_posY)[0], graphToReal(self.points[0].graph_posX, self.points[0].graph_posY)[1] , width=2, fill="IndianRed1");

	def delete(self, event):
		del graph.polygons[graph.polygons.index(self)]
		self.l._img.grid_forget();
		self.l.label.grid_forget();
		self.l.quitLabel.grid_forget();
		graph.show();

	def showLeftLabel(self):
		#self.l.text = str(self.name) + "(x) = " + str(self.expression);
		self.l.show();
		self.l.quitLabel.bind("<Button-1>", self.delete)



class Function():
	def __init__(self, name, expression, color):
		self.name = name;
		self.expression = expression;
		self.color = color;
		self.l = LeftFrameLabel(str(self.name) + "(x) = " + str(self.expression));
		#self.l.quitLabel.bind("<Button-1>", self.delete)

	def delete(self, event):
		del graph.functions[graph.functions.index(self)]
		self.l._img.grid_forget();
		self.l.label.grid_forget();
		self.l.quitLabel.grid_forget();
		graph.show();

	def showLeftLabel(self):
		self.l.text = str(self.name) + "(x) = " + str(self.expression);
		self.l.show();
		self.l.quitLabel.bind("<Button-1>", self.delete)



class Point:
	def __init__(self, posX, posY, name):
		self.graph_posX = posX;
		self.graph_posY = posY;
		self.posZ=0;
		self.name=name;
		self.size = 7;
		self.l=LeftFrameLabel( name + " = (" + str(self.graph_posX)+ "," + str(self.graph_posY)+")" );

	def show(self):
		rotationZ = [
			[math.cos(angle[2]), -math.sin(angle[2]), 0],
			[math.sin(angle[2]), math.cos(angle[2]), 0],
			[0, 0, 1],
		];

		rotationX = [
			[1, 0, 0],
			[0, math.cos(angle[0]), -math.sin(angle[0])],
			[0, math.sin(angle[0]), math.cos(angle[0])],
		];

		rotationY = [
			[math.cos(angle[1]), 0, math.sin(angle[1])],
			[0, 1, 0],
			[-math.sin(angle[1]), 0, math.cos(angle[1])],
		];

		projected=[];
		rotated = numpy.dot(rotationY, [self.graph_posX, self.graph_posY, self.posZ]);
		rotated = numpy.dot(rotationX, rotated);
		rotated = numpy.dot(rotationZ, rotated);
		projected2d = numpy.dot(projection, rotated);
		
		self.real_posX = graphToReal(projected2d[0], projected2d[1])[0];
		self.real_posY = graphToReal(projected2d[0], projected2d[1])[1];

		
		w.create_oval(self.real_posX - self.size/2 , self.real_posY - self.size/2 , self.real_posX + self.size/2,  self.real_posY + self.size/2, width=1, fill = 'thistle2');
		w.create_text(self.real_posX , self.real_posY-self.size*2 ,fill="dark orange",font="Arial", activefill="#000000", text=self.name);
		self.l.label.config(text= self.name + " = (" + str(self.graph_posX)+ "," + str(self.graph_posY)+")");

	def delete(self, event):
		del graph.points[graph.points.index(self)]
		self.l._img.grid_forget();
		self.l.label.grid_forget();
		self.l.quitLabel.grid_forget();
		graph.show();

	def pointPreference(self):
		def apply_button():
			self.graph_posX  = float(self.xEntry.get())
			self.graph_posY  = float(self.yEntry.get())
			self.posZ = float(self.zEntry.get());
			self.name  = self.nameEntry.get()
			#self.l.text = self.name + " = (" + str(self.graph_posX)+ "," + str(self.graph_posY)+")";
			self.l.label.config(text= self.name + " = (" + str(self.graph_posX)+ "," + str(self.graph_posY)+")");
			self.size = self.sizeScale.get()
			graph.show();


		self.preference_root =  Toplevel(root)
		self.preference_root.title("Geogebra revisité")

		self.nameLabel = Label(self.preference_root, text="Name");
		self.nameLabel.grid(row=0, column=0);

		self.nameEntry = Entry(self.preference_root, text=str(self.name));
		self.nameEntry.grid(row=0, column=1);
		self.nameEntry.delete(0, "end")
		self.nameEntry.insert(0, str(self.name))

		self.x = Label(self.preference_root, text="x")
		self.x.grid(row=1, column=1);

		self.y = Label(self.preference_root, text="y")
		self.y.grid(row=1, column=2);

		self.z = Label(self.preference_root, text="z")
		self.z.grid(row=1, column=3);

		self.position = Label(self.preference_root, text="Position")
		self.position.grid(row=2, column=0);

		self.xEntry = Entry(self.preference_root, text="x");
		self.xEntry.grid(row=2, column=1);
		self.xEntry.delete(0, "end")
		self.xEntry.insert(0, str(self.graph_posX))


		self.yEntry = Entry(self.preference_root, text="y");
		self.yEntry.grid(row=2, column=2);
		self.yEntry.delete(0, "end")
		self.yEntry.insert(0, str(self.graph_posY))
		
		self.zEntry = Entry(self.preference_root, text="z");
		self.zEntry.grid(row=2, column=3);
		self.zEntry.delete(0, "end")
		self.zEntry.insert(0, str(self.posZ))
		


		self.y = Label(self.preference_root, text="Point Size")
		self.y.grid(row=3, column=0);

		self.sizeScale = Scale(self.preference_root, from_=0, to=20,  orient=HORIZONTAL)
		self.sizeScale.set(7)
		self.sizeScale.grid(row=3, column=1);


		'''
		gap_slider = Scale(preference_root, from_=1, to=50, orient=HORIZONTAL)
		gap_slider.set(25)
		gap_slider.grid(row=0, column=1);
	'''
		self.apply_button = Button(self.preference_root, text="Apply", command=apply_button);
		self.apply_button.grid(row=10, column=0);




	def showLeftLabel(self):
		self.l.text = self.name + " = (" + str(self.graph_posX)+ "," + str(self.graph_posY)+")";
		self.l.show();
		self.l.quitLabel.bind("<Button-1>", self.delete)
		self.l.label.config(command=self.pointPreference)



def realToGraph(realX, realY):
	x, y = (realX-graph.real_originX)/graph.t, -(realY-graph.real_originY)/ graph.t;
	x = round(x, 2)
	y = round(y, 2)
	return [(x),  (y)]

def graphToReal(graphX, graphY):
	x, y = graph.real_originX + graphX * graph.t  ,   graph.real_originY + graphY * -graph.t;
	x = round(x, 2)
	y = round(y, 2)
	return [( x ), ( y )]



# |||||||||     Classe principale. |||||||||||||

class Graph:
    def __init__(self, graph_posX, graph_posY, real_originX, real_originY):
    	self.graph_posX = graph_posX;
    	self.graph_posY = graph_posY;
    	self.real_originX = real_originX;
    	self.real_originY = real_originY;
    	self.points = [];
    	self.functions = [];
    	self.polygons = [];
    	self.variables = [];
    	self.gap = 25;
    	self.t = 50;
    	self.lineCoef = [1,1]
    	self.state = "Placing-Points";

    def showFunctions(self):
    	# Pour highlight, on trace 1 seule ligne et pas plusieurs.
    	for f in range(len(self.functions)):
    		real_lastPointX, real_lastPointY = "NaN","NaN";
    		for i in range(int(self.graph_posX ), int(self.graph_posX +width)):
    			if (i%int(self.gap)==0):
    				try:
    					exp =  self.functions[f].expression.replace("x", "("+str(i/(self.t)  )+")");
    					for v in range(len(self.variables)):
    						exp = exp.replace(str(self.variables[v].name), "(" +str(self.variables[v].value)+")" );
    					image = eval( exp );

    					if (str(int(abs(image))).isdigit()):
    						real_X = i+self.real_originX;
    						real_Y = -image*self.t+self.real_originY;

    						w.create_oval(real_X-5/2, real_Y-5/2, real_X+5/2, real_Y+5/2)
    						if (real_lastPointX != "NaN"):
    							color = self.functions[f].color;
    							w.create_line(real_lastPointX, real_lastPointY, real_X, real_Y,  width=2,  fill =(color) )
    						real_lastPointX, real_lastPointY = real_X, real_Y;


    				except Exception as e: print(e)

    def showAxe(self):
        w.create_line(self.real_originX, 0, self.real_originX, height, width=3, fill="slate blue",  activefill="#ff0000" );
        w.create_line(0, self.real_originY, width, self.real_originY, width=3, fill="slate blue", activefill="#ff0000" );

        for i in range(int(self.graph_posX ), int(self.graph_posX +width)):
            '''
            if (i%(self.t) == 0 and i is not 0):
                s = 12;
                if ( int(i/self.t)%5 == 0):
                    s = 14;
                w.create_line(self.real_originX+1*i*self.lineCoef[0], 0, self.real_originX+i, height,    fill="gray22", activefill="#FFFFFF");
                w.create_text(self.real_originX+i, self.real_originY+10 ,font=('Arial', s, 'bold'), fill="gray99" , activefill="#000000", text=str(i/self.t));
            '''
            if (i%(self.t) == 0):
                w.create_line(self.real_originX+1*i*self.lineCoef[0], 0, self.real_originX+i, height,    fill="gray22", activefill="#FFFFFF");
            if (i%(self.gap*4) == 0):
                s = 12;
                if (i % int(self.t) == 0):
                    s = 14;
                w.create_text(self.real_originX+i, self.real_originY+10 ,font=('Arial', s, 'bold'), fill="gray99" , activefill="#000000", text=str(round(i/self.t, 2)));


        for i in range(int(self.graph_posY), int(self.graph_posY+height)):
            if (i%(self.t) == 0):
                 w.create_line(0, self.real_originY+i*self.lineCoef[1], width, self.real_originY+i, fill="gray22", activefill="#FFFFFF");
            if (i%(self.gap*4) == 0):
                s = 12;
                if (i % int(self.t) == 0):
                    s = 14;
                w.create_text(self.real_originX-20, self.real_originY+(i) ,font=('Arial', s, 'bold'), fill="gray99",activefill="#000000" , text=str(round(i/self.t*(-1),2) ));

    def showPoints(self):
    	for i in range(len(self.points)):
    		self.points[i].show();

    def showDebugHud(self):
    	w.create_text(200, 30,   fill="SpringGreen4",font=('Arial', 12, 'italic'), activefill="coral4", text="Debug HUD")
    	w.create_text(200, 100, fill="SpringGreen4",font=('Arial', 12, 'italic'), activefill="coral4" ,  text=" graph_pos("+ str(self.graph_posX) + "," + str(self.graph_posY) + ")\n real_origin(" + str(self.real_originX)+ "," + str(self.real_originY)  +")\n points: "+ str(len(self.points)) +"\n functions: " + str(len(self.functions)) + "\n variables: " + str(len(self.variables)) + "\n polygons:  " + str(len(self.polygons)) + "\n t: "+ str(self.t) + " graphstate: " + str(self.state) )

    def showPolygons(self):
    	for i in range(len(self.polygons)):
    		self.polygons[i].show();

    def show(self):
        w.delete("all")
        w.create_rectangle(0, 0, 1920, 1080, fill="gray4")
        self.showAxe();
        self.showPoints();
        self.showFunctions();
        self.showPolygons();
        self.showDebugHud();

graph = Graph(-width/2, -height/2, width/2, height/2);
graph.show();
'''
middleButtonPressed = False;
def middlebuttonpressed(event):
	middleButtonPressed = True;

def middlebuttonreleased(event):
	middleButtonPressed = False;

root.bind('<Button-2>', middlebuttonpressed);
root.bind('<ButtonRelease-2>', middlebuttonreleased);
'''

'''
def middlebuttonmoved(event):
	x, y = event.x, event.y
	graph.originX = x;
	graph.originY = y;

	#print('{}, {}'.format(x, y))
	graph.show();

def leftbuttonmoved(event):
	x, y = event.x, event.y
	print(graph.originX);

	if (x < 1000):
		graph.originX+=10;
	elif (x>1000):
		graph.originX-=10;
	graph.show();

root.bind('<B1-Motion>', leftbuttonmoved);

root.bind('<B2-Motion>', middlebuttonmoved); '''


# |||||||||    Prise en charge du clavier et de la souris. |||||||||||||



polygon_points = [];


def leftbuttonpressed(event):
	global polygon_points;
	x, y = event.x, event.y;
	graph_posX, graph_posY = realToGraph(x,y)[0], realToGraph(x,y)[1]
	if (graph.state == "Placing-Points"):
		p = Point(graph_posX, graph_posY, str(alphabet[len(graph.points)%26]))
		graph.points.append(p)
		p.showLeftLabel();
		#print("Réel ", str(x), str(y))
		#print("Graph :"+  str(realToGraph(x, y)) )
	elif (graph.state == "Placing-Polygon-Points"):
		if (len(polygon_points) > 1 and int(polygon_points[0].graph_posX) >= int(graph_posX-0.2) and int(polygon_points[0].graph_posX) <= int(graph_posX+0.2) and int(polygon_points[0].graph_posY) >= int(graph_posY-0.2) and int(polygon_points[0].graph_posY) <= int(graph_posY+0.2)):
			polygon = Polygon(polygon_points);
			graph.polygons.append(polygon);
			polygon.showLeftLabel();
			polygon_points=[]
		else:
			p = Point(graph_posX, graph_posY, "P"+str(alphabet[len(graph.polygons)%26])+"_"+ str(alphabet[len(polygon_points)%26]))
			graph.points.append(p)
			p.showLeftLabel();
			polygon_points.append(p)
	graph.show()




w.bind('<Button-1>', leftbuttonpressed);
def leftKey(event):
	graph.t+=10;
	'''graph.originX+=50;
	graph.posX-=50;'''
	graph.show();

def rightKey(event):
	graph.t-=10;
	'''graph.originX-=50;
	graph.posX+=50;'''
	graph.show();

def upKey(event):
    graph.real_originY+=50;
    graph.graph_posY-=50;

    graph.show();

def downKey(event):
	graph.real_originY-=50;
	graph.graph_posY+=50;
	graph.show();

def keydown(event):
	global angle;
	if (event.char == 'z'):
		graph.real_originY+=100;
		graph.graph_posY-=100;
	elif (event.char == 's'):
		graph.real_originY-=100;
		graph.graph_posY+=100;
	elif (event.char == 'd'):
		graph.real_originX-=100;
		graph.graph_posX+=100;
	elif (event.char == 'q'):
		graph.real_originX+=100;
		graph.graph_posX-=100;
	elif (event.char == 'e'):
		graph.t+=10;
	elif (event.char == 'r'):
		graph.t-=10;
	elif (event.char == "i"):
		graph.lineCoef[1]+=0.2;
	elif (event.char == "k"):
		graph.lineCoef[1]-=0.2;
	elif (event.char == "j"):
		graph.lineCoef[0]-=0.2;
	elif (event.char == "l"):
		graph.lineCoef[0]+=0.2;
	elif (event.char == "c"):
		angle[0]+=0.11;
	elif (event.char == "v"):
		angle[1]+=0.11;
	elif (event.char == "b"):
		angle[2]+=0.11;
	elif (event.char == "n"):
		angle = [0, 0, 0]
		graph.lineCoef = [1, 1]
	graph.show();


def scroll_in(event):
	graph.t+=10;
	graph.show();

def scroll_out(event):
	graph.t-=10;
	graph.show();



root.bind('<Up>', upKey)
root.bind('<Down>', downKey)
root.bind("<KeyPress>", keydown)

'''
# SCROLL à la souris (w = canvas)
#  Windows
w.bind_all("<MouseWheel>", scroll_out)
#  Linux
w.bind("<Button-4>", scroll_in)
w.bind("<Button-5>", scroll_out) '''

# |||||||||         PREFERENCES |||||||||||||
def preference_window():
	def apply_button():
		graph.gap = int(gap_slider.get())
		graph.show();
	preference_root =  Toplevel(root)

	gap_label = Label(preference_root, text="Espace entre chaque point");
	gap_label.grid(row=0, column=0);

	gap_slider = Scale(preference_root, from_=1, to=50, orient=HORIZONTAL)
	gap_slider.set(25)
	gap_slider.grid(row=0, column=1);

	apply_button = Button(preference_root, text="Apply", command=apply_button);
	apply_button.grid(row=2, column=0);




# |||||||||    TOP MENU  |||||||||||||

def createVariable():
	variable = Variable();
	graph.variables.append(variable);
	variable.showLeftLabel();





menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="Preferences", menu=filemenu)
filemenu.add_command(label="Options", command=preference_window)

pointsMenu = Menu(menu)
menu.add_cascade(label="Points", menu=pointsMenu)
pointsMenu.add_command(label="Place", command = lambda: setGraphStateTo("Placing-Points"))
pointsMenu.add_command(label="Variable",  command = createVariable)


polygonMenu = Menu(menu)
menu.add_cascade(label="Polygon", menu=polygonMenu )
polygonMenu.add_command(label="Place",  command = lambda: setGraphStateTo("Placing-Polygon-Points"))



def setGraphStateTo(state):
	global polygon_points
	graph.state=state;
	print(state);
	polygon_points=[];

#filemenu.add_separator()







root.mainloop()
