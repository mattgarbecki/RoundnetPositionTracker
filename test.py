import js2py

js = """
let accelerometer = new Accelerometer({frequency: 60});
function escramble_758(){
var a,b,c
a=1
b=2
c=3
document.write(a+c+b)
}
escramble_758()
""".replace("document.write", "return ")

result = js2py.eval_js(js)
print(result)