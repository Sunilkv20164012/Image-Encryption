from PIL import Image
import hashlib
import textwrap
import numpy as np 
import math
img = Image.open('image_encryp/images.jpg')
m, n = img.size
width, height = m, n
print("pixels: {0}  width: {2} height: {1} ".format(m*n, m, n))
pix = img.load()          
plainimage = list()                         #_plainimage contains all the rgb values continuously

for y in range(n):
    for x in range(m):
        for k in range(0,3):
            plainimage.append(pix[x,y][k])   

key = hashlib.sha512()                      #key is made a hash.sha256 object 
key.update(bytearray(plainimage))           #image data is fed to generate digest
key=key.hexdigest() 
key_bin = bin(int(key, 16))[2:].zfill(256)  #converting  in binary sequence
print (len(key_bin))                        #checking 256 character in hash key

pxs = []
for y in range(m):
    for x in range(n):
        pxs.append(img.getpixel((x, y)))

ans = [list(i) for i in pxs]
imgl = [list(i) for i in ans]
print (len(ans))

tmp = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(tmp)
image.save('image_encryp/original.jpg')
print("Saved original.")

original = [[imgl[i][k] for k in range(3)] for i in range(256*256)]
print(original[0])


#-----------------GEnerating chaotic sequence----------------------------------

x0=y0=z0=w0=0.00000005
k={}                                        #key dictionary
key_64_parts=textwrap.wrap(key_bin, 8)      #slicing key into 8-8 parts
# print(key_64_parts)
num=1
for i in key_64_parts:
    k["k{0}".format(num)]=i
    num=num+1
# print(k)                                   # k1, k2, k3....k64 created

# print(int(k["k{0}".format(1)],2))
h1 = h2 = h3 = h4 = 0
for i in range (1,4):
    h1=h1^int(k["k{0}".format(i)],2)
for i in range (4,7):
    h1=h1+int(k["k{0}".format(i)],2)

for i in range (7,10):
    h2=h2^int(k["k{0}".format(i)],2)
for i in range (10,13):
    h2=h2+int(k["k{0}".format(i)],2)

for i in range (13,16):
    h3=h3^int(k["k{0}".format(i)],2)
for i in range (16,19):
    h3=h3+int(k["k{0}".format(i)],2)

for i in range (19,22):
    h4=h4^int(k["k{0}".format(i)],2)
for i in range (22,25):
    h4=h4+int(k["k{0}".format(i)],2)


h1=float(float(h1)/256)
h2=float(float(h2)/256)
h3=float(float(h3)/256)
h4=float(float(h4)/256)

L = (256*256)
a1 = [0]*L
a2 = [0]*L
a3 = [0]*L
a4 = [0]*L

b1 = [0]*L
b2 = [0]*L
b3 = [0]*L
b4 = [0]*L

print(type(h1))
for i in range(0,L):
    a1[i]=x0+abs(round(h1)-h1)
    x0=a1[i]
    b1[i]= a1[i]-int(a1[i])

for i in range(0,L):
    a2[i]=y0+abs(round(h2)-h2)
    y0=a2[i]
    b2[i]= a2[i]-int(a2[i])

for i in range(0,L):
    a3[i]=z0+abs(round(h3)-h3)
    z0=a3[i]
    b3[i]= a3[i]-int(a3[i])

for i in range(0,L):
    a4[i]=w0+abs(round(h4)-h4)
    w0=a4[i]
    b4[i]= ((a4[i]-int(a4[i]))*10000)%256
    b4[i]=int(b4[i])

print("b4",b4[0])

print("b4",b4[1])
print("b4",b4[2])
print("b4",b4[3])


#------------------------------------------------------------------
#--------------Constructing Hill encryption matrix----------------

# Sample M
# M = [[0 for i in range(4)] for j in range(4)] 
# M = ([b4[0],b4[1],1-b4[0], -b4[1]], [b4[2], b4[3], -b4[2], 1-b4[3]], [1+b4[0], b4[1], -b4[0], -b4[1]], [b4[2], 1+b4[3],-b4[2], -b4[3]])

# ------------------hill encryption----------------------------------

for i in range(0,65536,4):
    for j in range(0,3):
        
        Q=([imgl[i][j]], [imgl[i+1][j]], [imgl[i+2][j]], [imgl[i+3][j]])
        M = ([b4[i+0],b4[i+1],1-b4[i+0], -b4[i+1]], [b4[i+2], b4[i+3], -b4[i+2], 1-b4[i+3]], [1+b4[i+0], b4[i+1], -b4[i+0], -b4[i+1]], [b4[i+2], 1+b4[i+3],-b4[i+2], -b4[i+3]])
        res = np.dot(M,Q)
  
        imgl[i][j]= int(res[0][0]%256)
        imgl[i+1][j]= int(res[1][0]%256)
        imgl[i+2][j]= int(res[2][0]%256)
        imgl[i+3][j] = int(res[3][0]%256)
        
        
# print(imgl[0])
imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/2.jpg')
print("Saved image2.")


# ----------------------------scramble the pixel position 1st & generate I3-----------------


po = 10**8
for i in range(1, 256):
    for j in range(1, 256):
        for k in range(3):
            i1 = i + (int(math.floor(b1[i*256+j]*po)) % (height-i))
            j1 = j + (int(math.floor(b1[i*256+j]*po)) % (width-j))
            imgl[i*height+j][k],imgl[i1*height+j1][k] = imgl[i1*height+j1][k],imgl[i*height+j][k]


imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/3.jpg')
print("Saved image3.")

# ------------------------------------------DECRYPT Pixel Scrambling-------------------------

# po = 10**8
# for i in range(255,-1,-1):
#     for j in range(255,-1,-1):
#         for k in range(3):
#             i1 = i + (int(math.floor(b1[i*256+j]*po)) % (height-i))
#             j1 = j + (int(math.floor(b1[i*256+j]*po)) % (width-j))
#             imgl[i*height+j][k],imgl[i1*height+j1][k] = imgl[i1*height+j1][k],imgl[i*height+j][k]


# imgl1 = [tuple(i) for i in imgl]
# OUTPUT_IMAGE_SIZE = (256, 256)
# image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
# image.putdata(imgl1)
# image.save('image_encryp/dec3.jpg')
# print("Saved dec 3.")

# ------------------------------------------END OF DECRYPT Pixel Scrambling-------------------------
# ------------------------------------------DECRYPT Hill Cypher-------------------------

# for i in range(0,65536,4):
#     for j in range(0,3):
        
#         Q=([imgl[i][j]], [imgl[i+1][j]], [imgl[i+2][j]], [imgl[i+3][j]])
        
#         M = ([b4[i+0],b4[i+1],1-b4[i+0], -b4[i+1]], [b4[i+2], b4[i+3], -b4[i+2], 1-b4[i+3]], [1+b4[i+0], b4[i+1], -b4[i+0], -b4[i+1]], [b4[i+2], 1+b4[i+3],-b4[i+2], -b4[i+3]])

#         res = np.dot(M,Q)

#         imgl[i][j]=int(res[0][0]%256)
#         imgl[i+1][j]= int(res[1][0]%256)
#         imgl[i+2][j]= int(res[2][0]%256)
#         imgl[i+3][j] = int(res[3][0]%256)
        
# imgl1 = [tuple(i) for i in imgl]
# OUTPUT_IMAGE_SIZE = (256, 256)
# image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
# image.putdata(imgl1)
# image.save('image_encryp/dec2.jpg')
# print("Saved image decrypted 2.")


# -----------------------------------END OF DECRYPT Hill Cypher-------------------------


#----------------------------------------Analysis----------------------------------------------


#----------------------------------------Histgram-----------------------------
import matplotlib
import matplotlib.pyplot as plt
from numpy import cov

# x = [0 for i in range(256*256)]

# if imgl==original:
#     print("equal")

# print(original[0])
# print(imgl[0])

# for i in range(256):
#     for j in range(256):
#         x[i*256+j]=original[i*256+j][0]

# n, bins, patches = plt.hist(x=x, bins=256, color='#0504aa',alpha=0.7, rwidth=0.85)

# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('pixel value (for red in RGB)')
# plt.ylabel('Frequency')
# plt.title('Histogram for Encrypted image')
# maxfreq = n.max()
# plt.show()


#------------------------------------End of Histgram-----------------------------

#--------------------------------------Correlation---------------------------------

x=[i for i in range(2500)]
data1 = [0 for i in range(2500)]
data2 = [0 for i in range(2500)]

for i in range(2500-256-1):
    if (i%256)==255:
        continue
    data1[i]=imgl[i][0]
    data2[i]=imgl[(i+1)][0]

s = [4 for n in range(len(x))]
plt.scatter(data1,data2,s=s)
plt.show()

quit()

# n, bins, patches = plt.hist(x=data1, bins=256, color='#0504aa',alpha=0.7, rwidth=0.85)

# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('pixel value (for red in RGB)')
# plt.ylabel('Frequency')
# plt.title('Histogram for plain image')
# maxfreq = n.max()

# plt.plot(x,data1)
# plt.plot(x,data2)
# plt.show()



#----------------End of Correlation---------------------------------


#---------------------------------------- End Of Analysis----------------------------------------------


# ---------------------------DNA Encdoing Rules-----------------------------------------

dna = {}
dna1 ={}
dna1['00'] = 'A'     #Rule 1
dna1['01'] = 'C'
dna1['10'] = 'G'
dna1['11'] = 'T'

dna2 ={}
dna2['00'] = 'A'    #Rule2
dna2['01'] = 'G'
dna2['10'] = 'C'
dna2['11'] = 'T'

dna3 ={}
dna3['00'] = 'C'    #Rule 3
dna3['01'] = 'A'
dna3['10'] = 'T'
dna3['11'] = 'G'

dna4 ={}
dna4['00'] = 'G'    #Rule4
dna4['01'] = 'A'
dna4['10'] = 'T'
dna4['11'] = 'C'

dna5 ={}
dna5['00'] = 'C'    #Rule 5
dna5['01'] = 'T'
dna5['10'] = 'A'
dna5['11'] = 'G'

dna6 ={}
dna6['00'] = 'G'    #Rule 6
dna6['01'] = 'T'
dna6['10'] = 'A'
dna6['11'] = 'C'

dna7 ={}
dna7['00'] = 'T'    #Rule 7
dna7['01'] = 'C'
dna7['10'] = 'G'
dna7['11'] = 'A'

dna8 ={}
dna8['00'] = 'T'    #Rule 8
dna8['01'] = 'G'
dna8['10'] = 'C'
dna8['11'] = 'A'

dnacov ={}
dnacov['A'] = '00'
dnacov['T'] = '11'
dnacov['G'] = '10'
dnacov['C'] = '01'

# DNA xor
dnax ={}
dnax["AA"] = dnax["TT"] = dnax["GG"] = dnax["CC"] = 'A'
dnax["AG"] = dnax["GA"] = dnax["TC"] = dnax["CT"] = 'G'
dnax["AC"] = dnax["CA"] = dnax["GT"] = dnax["TG"] = 'C'
dnax["AT"] = dnax["TA"] = dnax["CG"] = dnax["GC"] = 'T'
# dna['cov']=dnacov
dna= {1: dna1, 2:dna2, 3:dna3, 4:dna4, 5:dna5, 6:dna6, 7:dna7, 8:dna8, 'cov':dnacov, 'xor':dnax}
# print( dna['xor']['AA'])

K="AGTTCCAGCAGATTTG"                # Hardcoded Key taken for F function need to be modified later

# ----------------------------[DNA Encoding->Feistel transformation -> DNA Decoding](round 1)------------------

for i in range(0,65536,8):
    for j in range(3):
        xx =""
        for k in range (8):
            n = imgl[i+k][j]
            # print(n)
            s = bin(n)
            # print(s)
            s=s[2:]
            # print(len(s1))
            le = len(s)
            while le != 8:
                s = '0' + s
                le = le + 1
            # print(s)
            ii=int(i/256)
            jj=int(i%256)
            # ii=0
            # jj=k
            rr=((ii-1)*256+jj)%8 +1
            s2 = s[:2]
            s3 = s[2:4]
            s4 = s[4:6]
            s5 = s[6:8]
            # print(rr)
            g2 = dna[rr].get(s2)
            g3 = dna[rr].get(s3)
            g4 = dna[rr].get(s4)
            g5 = dna[rr].get(s5)
            xx = xx+ (g2+g3+g4+g5)
        L=xx[0:16]
        R=xx[16:]    
        # print(L)
        # print(R)
        # print (xx)
        L1=R
        R1=""
        for k in range(16):
            s1=R[k]+K[k]
            # print(s1)
            s2=L[k]+dna['xor'][s1]
            R1=R1+dna['xor'][s2]
            # print(R1)
        xx=L1+R1
        # print(xx)

        for k in range (8):
            s2 = xx[(k*4)]
            s3 = xx[(k*4)+1]
            s4 = xx[(k*4)+2]
            s5 = xx[(k*4)+3]
            s6="0b"+dna['cov'][s2]+dna['cov'][s3]+dna['cov'][s4]+dna['cov'][s5]
            # print(s6)
            imgl[i+k][j]=int(s6, 2)
            # print(imgl[i+k][j])

imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/4.jpg')
print("Saved image4.")

# ----------------------------scramble the pixel position 2nd & generate I5-----------------
ans = [list(i) for i in imgl]
# print (ans[0])
# print (imgl[0])
po = 10**15
for i in range(1, 256):
    for j in range(1, 256):
        i1 = (i + int(math.floor(b1[i]*po)) % (height-i))
        j1 = (j + int(math.floor(b1[i]*po)) % (width-j))
        imgl[i*height+j][0], imgl[i*height+j][1], imgl[i*height+j][2] =  ans[i1 * height + j1][0], ans[i1 * height + j1][1], ans[i1 * height + j1][2]

imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/5.jpg')
print("Saved image5.")

# ----------------------------[DNA Encoding->Feistel transformation -> DNA Decoding](round 2)------------------
for i in range(0,65536,8):
    for j in range(3):
        xx =""
        for k in range (8):
            n = imgl[i+k][j]
            # print(n)
            s = bin(n)
            # print(s)
            s=s[2:]
            # print(len(s1))
            le = len(s)
            while le != 8:
                s = '0' + s
                le = le + 1
            # print(s)
            ii=int(i/256)
            jj=int(i%256)
            # ii=0
            # jj=k
            rr=((ii-1)*256+jj)%8 +1
            s2 = s[:2]
            s3 = s[2:4]
            s4 = s[4:6]
            s5 = s[6:8]
            # print(rr)
            g2 = dna[rr].get(s2)
            g3 = dna[rr].get(s3)
            g4 = dna[rr].get(s4)
            g5 = dna[rr].get(s5)
            xx = xx+ (g2+g3+g4+g5)
        L=xx[0:16]
        R=xx[16:]    
        # print(L)
        # print(R)
        # print (xx)
        L1=R
        R1=""
        for k in range(16):
            s1=R[k]+K[k]
            # print(s1)
            s2=L[k]+dna['xor'][s1]
            R1=R1+dna['xor'][s2]
            # print(R1)
        xx=L1+R1
        # print(xx)

        for k in range (8):
            s2 = xx[(k*4)]
            s3 = xx[(k*4)+1]
            s4 = xx[(k*4)+2]
            s5 = xx[(k*4)+3]
            s6="0b"+dna['cov'][s2]+dna['cov'][s3]+dna['cov'][s4]+dna['cov'][s5]
            # print(s6)
            imgl[i+k][j]=int(s6, 2)
            # print(imgl[i+k][j])

imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/6.jpg')
print("Saved image6.")

# ----------------------------scramble the pixel position 3rdd & generate I7-----------------

ans = [list(i) for i in imgl]
po = 10**15
for i in range(1, 256):
    for j in range(1, 256):
        i1 = (i + int(math.floor(b1[i]*po)) % (height-i))
        j1 = (j + int(math.floor(b1[i]*po)) % (width-j))
        imgl[i*height+j][0], imgl[i*height+j][1], imgl[i*height+j][2] =  ans[i1 * height + j1][0], ans[i1 * height + j1][1], ans[i1 * height + j1][2]

imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/7.jpg')
print("Saved image7.")

# ----------------------------[DNA Encoding->Feistel transformation -> DNA Decoding](round 3)------------------
for i in range(0,65536,8):
    for j in range(3):
        xx =""
        for k in range (8):
            n = imgl[i+k][j]
            # print(n)
            s = bin(n)
            # print(s)
            s=s[2:]
            # print(len(s1))
            le = len(s)
            while le != 8:
                s = '0' + s
                le = le + 1
            # print(s)
            ii=int(i/256)
            jj=int(i%256)
            # ii=0
            # jj=k
            rr=((ii-1)*256+jj)%8 +1
            s2 = s[:2]
            s3 = s[2:4]
            s4 = s[4:6]
            s5 = s[6:8]
            # print(rr)
            g2 = dna[rr].get(s2)
            g3 = dna[rr].get(s3)
            g4 = dna[rr].get(s4)
            g5 = dna[rr].get(s5)
            xx = xx+ (g2+g3+g4+g5)
        L=xx[0:16]
        R=xx[16:]    
        # print(L)
        # print(R)
        # print (xx)
        L1=R
        R1=""
        for k in range(16):
            s1=R[k]+K[k]
            # print(s1)
            s2=L[k]+dna['xor'][s1]
            R1=R1+dna['xor'][s2]
            # print(R1)
        xx=L1+R1
        # print(xx)

        for k in range (8):
            s2 = xx[(k*4)]
            s3 = xx[(k*4)+1]
            s4 = xx[(k*4)+2]
            s5 = xx[(k*4)+3]
            s6="0b"+dna['cov'][s2]+dna['cov'][s3]+dna['cov'][s4]+dna['cov'][s5]
            # print(s6)
            imgl[i+k][j]=int(s6, 2)
            # print(imgl[i+k][j])

imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/8.jpg')
print("Saved image8.")

#--------------------------------------Ciphertext diffusion--------------------------------------------

for i in range(0,10):
    for j in range(3):
        if(i==0):
            imgl[i][j]= 127 ^ imgl[i][j]
        else:
            imgl[i][j]= imgl[i-1][j] ^ imgl[i][j]

# print (imgl[0])
# print (imgl[1])

# print (imgl[2])
# print (imgl[3])

# print (imgl[4])
# print (imgl[5])

# print (imgl[6])
# print (imgl[7])

imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/9.jpg')
print("Saved image9.")