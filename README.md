# Reveal and Auto-Hide 3D Cursor Addon V1.5.

A minor improvement to the 3D Cursor viewport overlay adding a bit more automation to the 3D Cursors visivbility. It would be awesome if it could be integrated into the Blender 2.8. 

# How it works
if the the 3D shortcut is pressed, it reveals the 3D Cursor but then when I press a different shortcut for a different tool, it automatically hides.  It’s a much better feature than assigning a shortcut and its really useful feature for other artists and save them from manually hiding and unhiding via viewport overlay too much. 

The add-on also respects the users who prefer the 3D Cursor visibility permanently on too via an if statement checking whether the 3d cursor is already visible or not.  If it is visible it just works as normal by setting the current tool to 3D Cursor. 

NOTE: THE 3D CURSOR MUST BE HIDDEN FIRST IN THE VIEWPORT OVERLAY.

# How to install
1. Download the Repository
2. Put the Reveal and Auto-Hide 3D Cursor Addon.py into the Addons folder in your Blender Directory  
3. Open Blender 2.8
4. go to Edit>Preferences
5. click on Addons tab 
6. Select the addon 
7. Hide the 3D Cursor in the Viewport overlay

# How to install
Press the back slash key to make it reveal the 3D Cursor and press a different shortcut for a different tool to Auto-Hide the 3D Cursor 

# Customisations
I have set the shortcut to Back slash ' \ ' key, feel free to change the shortcut via keymap. just remember to call the operator: wm.3dcursor_autovisibility 

It would be great if it could replace the existing shortcut for the 3D Cursor if it does get integrated into the blender build. Also, if anyone can suggest any improvements to enhance this add on further please let me know. Anyways keep making Blender even more awesome guys!!😀
