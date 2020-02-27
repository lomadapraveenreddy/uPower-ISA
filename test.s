.data
x: .word -5
y: .word 10
z: .word 0
.text
la r1,x
la r2,y
lwz r3,0(r1)
lwz r4,0(r2)
add r5,r3,r4
la r6,z
stw r5,0(r6)
lwz r7,0(r6)

