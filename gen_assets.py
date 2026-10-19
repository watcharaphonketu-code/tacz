import json, struct, zlib, os
A = 'src/main/resources/assets/taczbosses'

# ---------- geo ----------
def cube(o, s, uv): return {"origin": o, "size": s, "uv": uv}
bones = [
 {"name":"root","pivot":[0,0,0]},
 {"name":"right_leg","parent":"root","pivot":[-2,12,0],"cubes":[cube([-4,0,-2],[4,12,4],[0,16])]},
 {"name":"armorBipedRightLeg","parent":"right_leg","pivot":[-1.9,12,0]},
 {"name":"armorBipedRightFoot","parent":"right_leg","pivot":[-1.9,12,0]},
 {"name":"left_leg","parent":"root","pivot":[2,12,0],"cubes":[cube([0,0,-2],[4,12,4],[16,48])]},
 {"name":"armorBipedLeftLeg","parent":"left_leg","pivot":[1.9,12,0]},
 {"name":"armorBipedLeftFoot","parent":"left_leg","pivot":[1.9,12,0]},
 {"name":"body","parent":"root","pivot":[0,12,0],"cubes":[cube([-4,12,-2],[8,12,4],[16,16])]},
 {"name":"armorBipedBody","parent":"body","pivot":[0,24,0]},
 {"name":"head","parent":"body","pivot":[0,24,0],"cubes":[cube([-4,24,-4],[8,8,8],[0,0])]},
 {"name":"armorBipedHead","parent":"head","pivot":[0,24,0]},
 {"name":"right_arm","parent":"body","pivot":[-5,22,0],"cubes":[cube([-8,12,-2],[4,12,4],[40,16])]},
 {"name":"armorBipedRightArm","parent":"right_arm","pivot":[-5,22,0]},
 {"name":"weapon_right","parent":"right_arm","pivot":[-6,12,0]},
 {"name":"left_arm","parent":"body","pivot":[5,22,0],"cubes":[cube([4,12,-2],[4,12,4],[32,48])]},
 {"name":"armorBipedLeftArm","parent":"left_arm","pivot":[5,22,0]},
 {"name":"weapon_left","parent":"left_arm","pivot":[6,12,0]},
]
geo = {"format_version":"1.12.0","minecraft:geometry":[{
  "description":{"identifier":"geometry.boss","texture_width":64,"texture_height":64,
                 "visible_bounds_width":4,"visible_bounds_height":4,"visible_bounds_offset":[0,1,0]},
  "bones":bones}]}
json.dump(geo, open(f'{A}/geo/entity/boss.geo.json','w'), indent=1)

# ---------- animations ----------
anims = {}
def kf(d): return {str(k): v for k, v in d.items()}
def add(name, length, loop, bones):
    a = {"animation_length": length}
    if loop is True: a["loop"] = True
    elif loop == "hold": a["loop"] = "hold_on_last_frame"
    a["bones"] = {b: {k: kf(v) for k, v in d.items()} for b, d in bones.items()}
    anims["animation.boss." + name] = a

GUN_R = [-80,-8,0]; GUN_L = [-70,25,0]
add("idle", 2, True, {"body":{"position":{0:[0,0,0],1:[0,-0.3,0],2:[0,0,0]}}})
add("walk", 1, True, {
  "right_leg":{"rotation":{0:[0,0,0],0.25:[35,0,0],0.5:[0,0,0],0.75:[-35,0,0],1:[0,0,0]}},
  "left_leg":{"rotation":{0:[0,0,0],0.25:[-35,0,0],0.5:[0,0,0],0.75:[35,0,0],1:[0,0,0]}},
  "body":{"position":{0:[0,0,0],0.25:[0,0.5,0],0.5:[0,0,0],0.75:[0,0.5,0],1:[0,0,0]}}})
add("walk_back", 1.2, True, {
  "right_leg":{"rotation":{0:[0,0,0],0.3:[-25,0,0],0.6:[0,0,0],0.9:[25,0,0],1.2:[0,0,0]}},
  "left_leg":{"rotation":{0:[0,0,0],0.3:[25,0,0],0.6:[0,0,0],0.9:[-25,0,0],1.2:[0,0,0]}},
  "body":{"position":{0:[0,0,0],0.3:[0,0.4,0],0.6:[0,0,0],0.9:[0,0.4,0],1.2:[0,0,0]}}})
add("gun_hold", 1, True, {"right_arm":{"rotation":{0:GUN_R,1:GUN_R}},"left_arm":{"rotation":{0:GUN_L,1:GUN_L}}})
add("melee_hold", 1, True, {"right_arm":{"rotation":{0:[-30,0,0],1:[-30,0,0]}},"left_arm":{"rotation":{0:[-10,0,0],1:[-10,0,0]}}})
add("shoot", 0.2, False, {
  "body":{"rotation":{0:[0,0,0],0.04:[-4,0,0],0.2:[0,0,0]}},
  "right_arm":{"rotation":{0:GUN_R,0.04:[-86,-8,0],0.2:GUN_R}}})
add("reload", 1.5, False, {
  "left_arm":{"rotation":{0:GUN_L,0.3:[-30,40,0],0.9:[-30,40,0],1.2:[-75,20,0],1.5:GUN_L}},
  "right_arm":{"rotation":{0:GUN_R,0.3:[-60,-8,0],1.2:[-60,-8,0],1.5:GUN_R}},
  "body":{"rotation":{0:[0,0,0],0.3:[8,0,0],1.2:[8,0,0],1.5:[0,0,0]}}})
add("swing_a", 1.0, False, {
  "right_arm":{"rotation":{0:[-30,0,0],0.5:[-170,0,15],0.6:[-175,0,15],0.7:[-20,0,-10],1:[-30,0,0]}},
  "left_arm":{"rotation":{0:[-10,0,0],0.5:[-120,0,-10],0.7:[-30,0,0],1:[-10,0,0]}},
  "body":{"rotation":{0:[0,0,0],0.5:[-8,22,0],0.7:[14,-28,0],1:[0,0,0]}}})
add("swing_b", 0.9, False, {
  "right_arm":{"rotation":{0:[-30,0,0],0.4:[-90,50,70],0.55:[-90,-60,-10],0.9:[-30,0,0]}},
  "left_arm":{"rotation":{0:[-10,0,0],0.4:[-60,0,30],0.9:[-10,0,0]}},
  "body":{"rotation":{0:[0,0,0],0.4:[0,40,0],0.55:[0,-45,0],0.9:[0,0,0]}}})
add("spin", 1.0, False, {
  "body":{"rotation":{0:[0,0,0],0.35:[0,20,0],0.8:[0,-360,0],1:[0,-360,0]}},
  "right_arm":{"rotation":{0:[-30,0,0],0.35:[-90,0,80],0.8:[-90,0,80],1:[-30,0,0]}},
  "left_arm":{"rotation":{0:[-10,0,0],0.35:[-90,0,-80],0.8:[-90,0,-80],1:[-10,0,0]}}})
add("slam", 1.6, False, {
  "right_arm":{"rotation":{0:[-30,0,0],0.9:[-175,0,10],1.0:[-175,0,10],1.1:[-15,0,0],1.6:[-30,0,0]}},
  "left_arm":{"rotation":{0:[-10,0,0],0.9:[-170,0,-10],1.0:[-170,0,-10],1.1:[-15,0,0],1.6:[-10,0,0]}},
  "body":{"rotation":{0:[0,0,0],0.9:[-12,0,0],1.1:[25,0,0],1.6:[0,0,0]}}})
add("leap", 1.2, False, {
  "body":{"position":{0:[0,0,0],0.5:[0,-5,0],0.7:[0,3,0],1.2:[0,0,0]}},
  "right_leg":{"rotation":{0:[0,0,0],0.5:[-60,0,0],0.7:[10,0,0],1.2:[0,0,0]}},
  "left_leg":{"rotation":{0:[0,0,0],0.5:[-60,0,0],0.7:[10,0,0],1.2:[0,0,0]}},
  "right_arm":{"rotation":{0:[-30,0,0],0.5:[20,0,0],0.7:[-170,0,0],1.2:[-30,0,0]}},
  "left_arm":{"rotation":{0:[-10,0,0],0.5:[20,0,0],0.7:[-170,0,0],1.2:[-10,0,0]}}})
add("dash_warn", 1.0, "hold", {
  "body":{"rotation":{0:[0,0,0],0.4:[25,0,0],1:[30,0,0]},"position":{0:[0,0,0],0.4:[0,-2,0],1:[0,-2.5,0]}},
  "right_leg":{"rotation":{0:[0,0,0],0.4:[-30,0,0],1:[-30,0,0]}},
  "left_leg":{"rotation":{0:[0,0,0],0.4:[20,0,0],1:[20,0,0]}}})
add("throw", 0.7, False, {
  "right_arm":{"rotation":{0:[-30,0,0],0.25:[-170,0,0],0.4:[-20,0,0],0.7:[-30,0,0]}},
  "body":{"rotation":{0:[0,0,0],0.25:[-10,0,0],0.4:[10,0,0],0.7:[0,0,0]}}})
add("shield", 0.5, "hold", {"left_arm":{"rotation":{0:[-10,0,0],0.3:[-90,-15,0],0.5:[-90,-15,0]}}})
add("kneel", 1, True, {
  "body":{"position":{0:[0,-5,0],1:[0,-5,0]}},
  "right_leg":{"rotation":{0:[-70,0,0],1:[-70,0,0]}},
  "left_leg":{"rotation":{0:[-100,0,0],1:[-100,0,0]}}})
add("sit_minigun", 1, True, {
  "body":{"position":{0:[0,-9,0],1:[0,-9,0]}},
  "right_leg":{"rotation":{0:[-90,0,10],1:[-90,0,10]}},
  "left_leg":{"rotation":{0:[-90,0,-10],1:[-90,0,-10]}},
  "right_arm":{"rotation":{0:[-75,-5,0],1:[-75,-5,0]}},
  "left_arm":{"rotation":{0:[-60,30,0],1:[-60,30,0]}}})
add("death", 1.5, "hold", {"root":{"rotation":{0:[0,0,0],1.0:[-90,0,0]},"position":{0:[0,0,0],1.0:[0,2,0]}}})
json.dump({"format_version":"1.8.0","animations":anims}, open(f'{A}/animations/entity/boss.animation.json','w'), indent=1)

# ---------- textures (flat colours, replace with real art later) ----------
def png(path, w, h, px):
    raw = b''.join(b'\x00' + b''.join(bytes(px(x, y)) for x in range(w)) for y in range(h))
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) \
         + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')
    open(path, 'wb').write(data)
base = [(84,98,58),(150,130,80),(70,72,76),(110,60,50),(40,50,90)]
for i, c in enumerate(base):
    def px(x, y, c=c):
        if 8 <= x < 16 and 11 <= y < 14: return (226,75,58,255)    # red visor strip on the head's front face
        if y < 16 and x < 32: return (c[0]//2+30, c[1]//2+30, c[2]//2+30, 255)
        return (c[0], c[1], c[2], 255)
    png(f'{A}/textures/entity/boss_{i+1}.png', 64, 64, px)
print('assets ok')
