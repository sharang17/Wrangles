import scipy as sc
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def error(f,x,y):
    return sc.sum((f(x)-y)**2)




web_data=sc.genfromtxt("web_traffic.tsv",delimiter="\t")
x=web_data[:,0]
y=web_data[:,1]
x=x[~sc.isnan(y)]
y=y[~sc.isnan(y)]
fx=sc.linspace(0,x[-1],1000)
#print sc.sum(sc.isnan(y))
#x=([w*7*24 for w in range(10)],['week %i' %w for w in range(10)])
#print x
plt.scatter(x,y,color="red",alpha=0.1)
plt.title("Web Traffic over last month")
plt.xlabel("Time")
plt.ylabel("Hits/Hour")
plt.xticks([w*7*24 for w in range(10)],['week %i'%w for w in range(10)])
plt.autoscale(axis='both')
#plt.grid()
#plt.show()


#polynomial of degree 1
fp1,residuals,rank,sv,rcond=sc.polyfit(x,y,1,full=True)
f1=sc.poly1d(fp1)
print "Error degree 1: %s " %str(error(f1,x,y))
#polynomial of degree 2
fp2=sc.polyfit(x,y,2)
f2=sc.poly1d(fp2)
print "Error degree 2: %s"%str(error(f2,x,y))
#polynomial of degree 3
fp3=sc.polyfit(x,y,3)
f3=sc.poly1d(fp3)
print "Error degree 3: %s"%str(error(f3,x,y))
#polynomial of degree 10
fp10=sc.polyfit(x,y,10)
f10=sc.poly1d(fp10)
print "Error degree 10: %s"%str(error(f10,x,y))
#polynomial of degree 100
fp100=sc.polyfit(x,y,100)
f100=sc.poly1d(fp100)
print "Error degree 100: %s"%str(error(f100,x,y))

plt.plot(fx, f1(fx),"b--",fx,f2(fx),"g:",fx,f3(fx),"y--",fx,f10(fx),"m--",fx,f100(fx),"k--")
plt.legend(["d=%i" % f1.order,"d=%i" % f2.order,"d=%i" % f3.order,"d=%i" % f10.order,"d=%i" % f100.order], loc="upper left")
plt.show()


inflection_point=3.5*7*24
xa=x[:inflection_point]
ya=y[:inflection_point]
xb=x[inflection_point:]
yb=y[inflection_point:]
fpa=sc.polyfit(xa,ya,1)
fpb=sc.polyfit(xb,yb,1)
fa=sc.poly1d(fpa)
fb=sc.poly1d(fpb)
fa_error=error(fa,xa,ya)
fb_error=error(fb,xb,yb)
fx_a=fx[:inflection_point]
fx_b=fx[inflection_point:]
plt.plot(fx_a,fa(fx_a),"b--",fx_b,fb(fx_b),"g--")
plt.show()
