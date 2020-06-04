from PIL import Image
import hashlib
import textwrap
import numpy as np 
import math
img = Image.open('image_encryp/9.png')
m, n = img.size
width, height = m, n
print("pixels: {0}  width: {2} height: {1} ".format(m*n, m, n))
pix = img.load()          
plainimage = list()                         #_plainimage contains all the rgb values continuously

for y in range(n):
    for x in range(m):
        for k in range(0,3):
            plainimage.append(pix[x,y][k])   


pxs = []
for y in range(m):
    for x in range(n):
        pxs.append(img.getpixel((x, y)))

ans = [list(i) for i in pxs]
imgl = [list(i) for i in ans]
for i in range(0,16):
    print(imgl[i][0])


tmp = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(tmp)
image.save('image_encryp/received.png')
print("Saved dec1.")

file1 = open("image_encryp/HexDigest.txt","r")
key=file1.read()                            #reading hexdigest from file
file1.close()
key_bin = bin(int(key, 16))[2:].zfill(256)  #converting  in binary sequence
# print(key_bin)

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


#-------------------------------------------------------------------------------------------



# ---------------------------DNA Encdoing Rules-----------------------------------------

dna = {}
dna1 ={}
dna1['A'] = '00'     #Rule 1
dna1['C'] = '01'
dna1['G'] = '10'
dna1['T'] = '11'

dna2 ={}
dna2['A'] = '00'    #Rule2
dna2['G'] = '01'
dna2['C'] = '10'
dna2['T'] = '11'

dna3 ={}
dna3['C'] = '00'    #Rule 3
dna3['A'] = '01'
dna3['T'] = '10'
dna3['G'] = '11'

dna4 ={}
dna4['G'] = '00'    #Rule4
dna4['A'] = '01'
dna4['T'] = '10'
dna4['C'] = '11'

dna5 ={}
dna5['C'] = '00'    #Rule 5
dna5['T'] = '01'
dna5['A'] = '10'
dna5['G'] = '11'

dna6 ={}
dna6['G'] = '00'    #Rule 6
dna6['T'] = '01'
dna6['A'] = '10'
dna6['C'] = '11'

dna7 ={}
dna7['T'] = '00'    #Rule 7
dna7['C'] = '01'
dna7['G'] = '10'
dna7['A'] = '11'

dna8 ={}
dna8['T'] = '00'    #Rule 8
dna8['G'] = '01'
dna8['C'] = '10'
dna8['A'] = '11'

dnacov ={}
dnacov['00'] = 'A'
dnacov['11'] = 'T'
dnacov['10'] = 'G'
dnacov['01'] = 'C'

# DNA xor
dnax ={}
dnax["AA"] = dnax["TT"] = dnax["GG"] = dnax["CC"] = 'A'
dnax["AG"] = dnax["GA"] = dnax["TC"] = dnax["CT"] = 'G'
dnax["AC"] = dnax["CA"] = dnax["GT"] = dnax["TG"] = 'C'
dnax["AT"] = dnax["TA"] = dnax["CG"] = dnax["GC"] = 'T'
# dna['cov']=dnacov
dnad= {1: dna1, 2:dna2, 3:dna3, 4:dna4, 5:dna5, 6:dna6, 7:dna7, 8:dna8, 'cov':dnacov, 'xor':dnax}
# print( dna['xor']['AA'])

K="AGTTCCAGCAGATTTG"                # Hardcoded Key taken for F function need to be modified later

#---------------------------------------------------------------------------------------------------------



#--------------------------------------Ciphertext diffusion--------------------------------------------

for i in range(65535,-1,-1):
    for j in range(3):
        if(i==0):
            imgl[i][j]= 127 ^ imgl[i][j]
        else:
            imgl[i][j]= imgl[i-1][j] ^ imgl[i][j]


imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/dec9.png')
print("Saved image decrypt Ciphertext diffusion 9.")


#--------------------------------------------------------------------------------------------------------------------------




# ----------------------------Decryption  [DNA Encoding->Feistel transformation -> DNA Decoding](round 1)------------------

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
            s2 = s[:2]
            s3 = s[2:4]
            s4 = s[4:6]
            s5 = s[6:8]

            xx = xx + (dnad['cov'][s2]+dnad['cov'][s3]+dnad['cov'][s4]+dnad['cov'][s5])
        
        # Fiestal one round
        L=xx[0:16]
        R=xx[16:]    
        # print(L)
        # print(R)
        # print (xx)
        L1=""
        R1=L
        for k in range(16):
            s1=R[k]+K[k]
            # print(s1)
            s2=L[k]+dnad['xor'][s1]
            L1=L1+dnad['xor'][s2]
            # print(R1)
        xx=L1+R1
        # print(xx)

        for k in range (8):
            s2 = xx[(k*4)]
            s3 = xx[(k*4)+1]
            s4 = xx[(k*4)+2]
            s5 = xx[(k*4)+3]
            
            ii=int(i/256)
            jj=int(i%256)
            # ii=0
            # jj=k
            rr=((ii-1)*256+jj)%8 +1
            g2 = dnad[rr].get(s2)
            g3 = dnad[rr].get(s3)
            g4 = dnad[rr].get(s4)
            g5 = dnad[rr].get(s5)
            s6="0b"+g2+g3+g4+g5

            imgl[i+k][j]=int(s6, 2)


imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/dec8.png')
print("Saved image dec dna encoding fiestal dna decoding 8.")

#---------------------------------------------------------------------------------------------------------


#------------------------------------------DECRYPT Pixel Scrambling-------------------------

po = 10**8
for i in range(255,-1,-1):
    for j in range(255,-1,-1):
        for k in range(3):
            i1 = i + (int(math.floor(b3[i*256+j]*po)) % (height-i))
            j1 = j + (int(math.floor(b3[i*256+j]*po)) % (width-j))
            imgl[i*height+j][k],imgl[i1*height+j1][k] = imgl[i1*height+j1][k],imgl[i*height+j][k]


imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/dec7.png')
print("Saved decrypt pixel scrambling using b3 7.")


#------------------------------------------END OF DECRYPT Pixel Scrambling-------------------------





# ----------------------------Decryption  [DNA Encoding->Feistel transformation -> DNA Decoding](round 1)------------------

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
            s2 = s[:2]
            s3 = s[2:4]
            s4 = s[4:6]
            s5 = s[6:8]

            xx = xx + (dnad['cov'][s2]+dnad['cov'][s3]+dnad['cov'][s4]+dnad['cov'][s5])
        
        # Fiestal one round
        L=xx[0:16]
        R=xx[16:]    
        # print(L)
        # print(R)
        # print (xx)
        L1=""
        R1=L
        for k in range(16):
            s1=R[k]+K[k]
            # print(s1)
            s2=L[k]+dnad['xor'][s1]
            L1=L1+dnad['xor'][s2]
            # print(R1)
        xx=L1+R1
        # print(xx)

        for k in range (8):
            s2 = xx[(k*4)]
            s3 = xx[(k*4)+1]
            s4 = xx[(k*4)+2]
            s5 = xx[(k*4)+3]
            
            ii=int(i/256)
            jj=int(i%256)
            # ii=0
            # jj=k
            rr=((ii-1)*256+jj)%8 +1
            g2 = dnad[rr].get(s2)
            g3 = dnad[rr].get(s3)
            g4 = dnad[rr].get(s4)
            g5 = dnad[rr].get(s5)
            s6="0b"+g2+g3+g4+g5

            imgl[i+k][j]=int(s6, 2)


imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/dec6.png')
print("Saved image dec dna encoding fiestal dna decoding 6.")

#---------------------------------------------------------------------------------------------------------


#------------------------------------------DECRYPT Pixel Scrambling-------------------------

po = 10**8
for i in range(255,-1,-1):
    for j in range(255,-1,-1):
        for k in range(3):
            i1 = i + (int(math.floor(b2[i*256+j]*po)) % (height-i))
            j1 = j + (int(math.floor(b2[i*256+j]*po)) % (width-j))
            imgl[i*height+j][k],imgl[i1*height+j1][k] = imgl[i1*height+j1][k],imgl[i*height+j][k]


imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/dec5.png')
print("Saved decrypt pixel scrambling using b2 5.")


#------------------------------------------END OF DECRYPT Pixel Scrambling-------------------------






# ----------------------------Decryption  [DNA Encoding->Feistel transformation -> DNA Decoding](round 1)------------------

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
            s2 = s[:2]
            s3 = s[2:4]
            s4 = s[4:6]
            s5 = s[6:8]

            xx = xx + (dnad['cov'][s2]+dnad['cov'][s3]+dnad['cov'][s4]+dnad['cov'][s5])
        
        # Fiestal one round
        L=xx[0:16]
        R=xx[16:]    
        # print(L)
        # print(R)
        # print (xx)
        L1=""
        R1=L
        for k in range(16):
            s1=R[k]+K[k]
            # print(s1)
            s2=L[k]+dnad['xor'][s1]
            L1=L1+dnad['xor'][s2]
            # print(R1)
        xx=L1+R1
        # print(xx)

        for k in range (8):
            s2 = xx[(k*4)]
            s3 = xx[(k*4)+1]
            s4 = xx[(k*4)+2]
            s5 = xx[(k*4)+3]
            
            ii=int(i/256)
            jj=int(i%256)
            # ii=0
            # jj=k
            rr=((ii-1)*256+jj)%8 +1
            g2 = dnad[rr].get(s2)
            g3 = dnad[rr].get(s3)
            g4 = dnad[rr].get(s4)
            g5 = dnad[rr].get(s5)
            s6="0b"+g2+g3+g4+g5

            imgl[i+k][j]=int(s6, 2)


imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/dec4.png')
print("Saved image dec dna encoding fiestal dna decoding 4.")

#---------------------------------------------------------------------------------------------------------


#------------------------------------------DECRYPT Pixel Scrambling-------------------------

po = 10**8
for i in range(255,-1,-1):
    for j in range(255,-1,-1):
        for k in range(3):
            i1 = i + (int(math.floor(b1[i*256+j]*po)) % (height-i))
            j1 = j + (int(math.floor(b1[i*256+j]*po)) % (width-j))
            imgl[i*height+j][k],imgl[i1*height+j1][k] = imgl[i1*height+j1][k],imgl[i*height+j][k]


imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/dec3.png')
print("Saved decrypt pixel scrambling using b1 3.")


#------------------------------------------END OF DECRYPT Pixel Scrambling-------------------------







#------------------------------------------DECRYPT Hill Cypher-------------------------

for i in range(0,65536,4):
    for j in range(0,3):
        
        Q=([imgl[i][j]], [imgl[i+1][j]], [imgl[i+2][j]], [imgl[i+3][j]])
        
        M = ([b4[i+0],b4[i+1],1-b4[i+0], -b4[i+1]], [b4[i+2], b4[i+3], -b4[i+2], 1-b4[i+3]], [1+b4[i+0], b4[i+1], -b4[i+0], -b4[i+1]], [b4[i+2], 1+b4[i+3],-b4[i+2], -b4[i+3]])

        res = np.dot(M,Q)

        imgl[i][j]=int(res[0][0]%256)
        imgl[i+1][j]= int(res[1][0]%256)
        imgl[i+2][j]= int(res[2][0]%256)
        imgl[i+3][j] = int(res[3][0]%256)

           
imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/dec2.png')
print("Saved image decrypted 2.")


#-----------------------------------END OF DECRYPT Hill Cypher-------------------------


          
imgl1 = [tuple(i) for i in imgl]
OUTPUT_IMAGE_SIZE = (256, 256)
image = Image.new('RGB', OUTPUT_IMAGE_SIZE)
image.putdata(imgl1)
image.save('image_encryp/decrypted_image.png')
print("Saved final decrypted image .")

