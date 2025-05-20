
obs = obslua
local socket = require("socket")
local host,port="127.0.0.1",7002
local udp=socket.udp()
udp:settimeout(0)
udp:setsockname(host,port)
function script_description() return "YOLO Aimbot HUD" end
function script_tick(sec)
  local data=udp:receive()
  if data then
    -- demo parse: AA x y btn crc 55
    local bytes={data:byte(1,#data)}
    local x=bytes[2]; local y=bytes[3]
    obs.remove_safe_texture("cross")
    obs.draw2d_texture("cross",x,y,16,16,0xffffff)
  end
end
