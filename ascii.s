.data
x: .word 3
as: .asciiz abcd
y: .word 4
sum: .word 0
.text
la r1,x
la r2,y
la r5,sum
lwz r3,0(r1)
lwz r4,0(r2)
add r6,r3,r4
stw r6,0(r5)
lwz r7,0(r5)
la r18,as
sc 4
