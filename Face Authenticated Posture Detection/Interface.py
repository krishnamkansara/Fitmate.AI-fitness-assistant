print("~~~~~ There are the Following Options Available ~~~~~~~\n(A) Curls (B) Squats (C) Deadlifts (D) Pushups ")
put = input("Enter Your Choice -->")

if put == 'A':
    import Curls
elif put== 'B':
    import Squats
elif put== 'C':
    import Deadlifts
elif put== 'D':
    import Pushups
else:
    exit()
   