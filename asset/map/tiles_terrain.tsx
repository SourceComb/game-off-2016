<?xml version="1.0" encoding="UTF-8"?>
<tileset name="tiles_terrain" tilewidth="32" tileheight="32" tilecount="256" columns="16">
 <image source="tiles_terrain.png" width="512" height="512"/>
 <terraintypes>
  <terrain name="plank_floor" tile="-1"/>
  <terrain name="plank_floor_edge_left" tile="-1"/>
  <terrain name="plank_floor_edge_right" tile="-1"/>
  <terrain name="plank_wall" tile="-1"/>
  <terrain name="plank_wall_edge_left" tile="-1"/>
  <terrain name="plank_wall_edge_right" tile="-1"/>
  <terrain name="log_vertical" tile="-1"/>
  <terrain name="log_horizontal" tile="-1"/>
 </terraintypes>
 <tile id="0" terrain="1,1,1,1">
  <properties>
   <property name="bottom" type="int" value="1"/>
   <property name="left" type="int" value="1"/>
   <property name="right" type="int" value="1"/>
   <property name="top" type="int" value="1"/>
  </properties>
 </tile>
 <tile id="1" terrain="0,0,0,0">
  <properties>
   <property name="bottom" type="int" value="1"/>
   <property name="left" type="int" value="1"/>
   <property name="right" type="int" value="1"/>
   <property name="top" type="int" value="1"/>
  </properties>
 </tile>
 <tile id="2" terrain="2,2,2,2">
  <properties>
   <property name="bottom" type="int" value="1"/>
   <property name="left" type="int" value="1"/>
   <property name="right" type="int" value="1"/>
   <property name="top" type="int" value="1"/>
  </properties>
 </tile>
 <tile id="4" terrain="6,6,6,6"/>
 <tile id="5" terrain="7,7,7,7"/>
 <tile id="16" terrain="1,1,1,1" probability="0.25">
  <properties>
   <property name="bottom" type="int" value="1"/>
   <property name="left" type="int" value="1"/>
   <property name="right" type="int" value="1"/>
   <property name="top" type="int" value="1"/>
  </properties>
 </tile>
 <tile id="17" terrain="0,0,0,0" probability="0.25">
  <properties>
   <property name="bottom" type="int" value="1"/>
   <property name="left" type="int" value="1"/>
   <property name="right" type="int" value="1"/>
   <property name="top" type="int" value="1"/>
  </properties>
 </tile>
 <tile id="18" terrain="2,2,2,2" probability="0.25">
  <properties>
   <property name="bottom" type="int" value="1"/>
   <property name="left" type="int" value="1"/>
   <property name="right" type="int" value="1"/>
   <property name="top" type="int" value="1"/>
  </properties>
 </tile>
 <tile id="20" terrain="6,6,6,6"/>
 <tile id="21" terrain="7,7,7,7"/>
 <tile id="32" terrain="4,4,4,4"/>
 <tile id="33" terrain="3,3,3,3"/>
 <tile id="34" terrain="5,5,5,5"/>
 <tile id="36" terrain="6,6,6,6"/>
 <tile id="37" terrain="7,7,7,7"/>
 <tile id="48" terrain="4,4,4,4" probability="0.25"/>
 <tile id="49" terrain="3,3,3,3" probability="0.25"/>
 <tile id="50" terrain="5,5,5,5" probability="0.25"/>
 <tile id="52" terrain="6,6,6,6"/>
 <tile id="53" terrain="7,7,7,7"/>
</tileset>
