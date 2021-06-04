# Short instruction on how to install an AppImage and create the desktop shortcut  

On a linux based system.  

Call this script with the **appimage path** and the **new name** the program (binary) should have afterwards.
`install-appimage.sh ~/Downloads/my-downloaded.AppImage installed-bin-name`  
On some ways on how to get this script on your computer see at the bottom of this page.  

```bash
START_DIR=$(pwd)
APP_IMG_PATH=$1
echo "Selected AppImage path to install to: "$APP_IMG_PATH
APP_IMG_NAME=$(basename $1)
echo "Name of the AppImage: "$APP_IMG_NAME
NEW_NAME=$2
echo "New name to be installed as: "$NEW_NAME

if [ -z $APP_IMG_PATH ]; then
    echo "Please pass a path to the appimage as argument! - exiting"
    exit 1
fi
if [ -z $NEW_NAME ]; then
    echo "Please pass an installation name as argument! - exiting"
    exit 1
fi
printf "\n" 
```

## Making the appimage executable

```bash
echo "Executing: chmod +x $APP_IMG_PATH"
chmod +x $APP_IMG_PATH
printf "\n"
```

## Move it to the temp directory and extract the appimage there

```bash
echo "Moving AppImage to: 'mv $APP_IMG_PATH /tmp'"
cp $APP_IMG_PATH /tmp
cd /tmp
echo "Executing: '$APP_IMG_NAME --appimage-extract'"
./$APP_IMG_NAME --appimage-extract
printf "\n"
```

## Find the desktop file in the extracted directory

```bash
echo "Executing: DESKTOP_FILE=find squashfs-root -name \"*.desktop\""
DESKTOP_FILE=$(find squashfs-root -name "*.desktop" | head -n 1)
echo "Found '$DESKTOP_FILE'"
printf "\n"
```

## And move it to your application links

```bash
DESKTOP_INSTALLED_DIR=~/.local/share/applications/
echo "Copy desktop file: 'cp $DESKTOP_FILE $DESKTOP_INSTALLED_DIR'"
cp $DESKTOP_FILE $DESKTOP_INSTALLED_DIR
DESKTOP_INSTALLED=$DESKTOP_INSTALLED_DIR$(basename $DESKTOP_FILE)
printf "\n"
```

## Then rename to appimage and move it to the user binaries directory

```bash
INSTALLED_PATH=~/.local/bin/$NEW_NAME
echo "Move binary: 'mv $APP_IMG_NAME $INSTALLED_PATH'"
mv $APP_IMG_NAME $INSTALLED_PATH
printf "\n"
```

## Use sed to replace the path of the executable in the desktop file

- **-i** to pass the files contents and edit in place
- **-E** enable extended regular expressions effectively enabling amount operators +*? and grouping
- **s** use sed to do a substitution
- **:** is selected as a delimiter to define what the searchterm and what the replaceterm is, we can choose that one (example /searchpattern/replacewith/ )
- Our search pattern is defined as a regular expression which matches a full line that starts with **Exec=**
- **w** write the result back to the source file  
- Then followed by the file path to `read from`/`write to`

```bash
echo "sed -i -E s:Exec=.+\n:Exec=$INSTALLED_PATH: $DESKTOP_INSTALLED"
sed -i -E s:Exec=.+:Exec=$INSTALLED_PATH: $DESKTOP_INSTALLED
printf "\n"
```

## Clean up extracted application temporary directory and go back to start dir

```bash
echo "Cleaning up"
rm -r /tmp/squashfs-root
cd $START_DIR
printf "\n"
echo "Finished installing $APP_IMG_NAME as $NEW_NAME!"
```

Now you are ready to start the application by looking for the desktop file or by
using your terminal and entering the new application name and hitting enter.

If you do not want to copy the sections of this script to a .sh file to exectute  
and instead want to run it directly from this page or install it on your computer permanently you  
can use **rnmd**.  

If you have pip (python modules installer) on your PC you can just do:  
`pip3 install rnmd`  

Or follow the instructions on the github page of the project:  
[rnmd github page](https://github.com/MarkusPeitl/rnmd)  

then you can run this page by:  
`rnmd https://www.github.com/MarkusPeitl/my-linux-scripts/docs/install-appimage.md --args ~/Downloads/my-downloaded.AppImage installed-bin-name`  

or install the script permanently to use it more often:  

**First time setup** of rnmd:  
`rnmd --setup`  
and follow the instructions.  

Then install the script.  
`rnmd www.github.com/MarkusPeitl/my-linux-scripts/docs/install-appimage.md --portableinstall appimageinstall`  

Then run the **appimageinstall** script whenever you need it:  
`appimageinstall ~/Downloads/my-downloaded.AppImage installed-bin-name`  

That was it i hope you liked this small guide.  
If you have any more questions just send me an email to:  
[office@markuspeitl.com](mailto:office@markuspeitl.com)

### If you like the article consider dropping me a coffee  

Maybe some crypto currency (redirects to a donation box on my blog):  
<a href="https://blog.markuspeitl.com/donate/"><img src="https://blog.markuspeitl.com/wp-content/plugins/cryptocurrency-donation-box/assets/logos/bitcoin.svg" width="50" /></a><a href="https://blog.markuspeitl.com/donate/"><img src="https://blog.markuspeitl.com/wp-content/plugins/cryptocurrency-donation-box/assets/logos/ethereum.svg" width="30" /></a><a href="https://blog.markuspeitl.com/donate/"><img src="https://blog.markuspeitl.com/wp-content/plugins/cryptocurrency-donation-box/assets/logos/xrp.svg" width="50" /></a><a href="https://blog.markuspeitl.com/donate/"><img src="https://blog.markuspeitl.com/wp-content/plugins/cryptocurrency-donation-box/assets/logos/stellar.svg" width="50" /></a><a href="https://blog.markuspeitl.com/donate/"><img src="https://blog.markuspeitl.com/wp-content/plugins/cryptocurrency-donation-box/assets/logos/litecoin.svg" width="50" /></a>

Or a coffee via paypal:  
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?hosted_button_id=BSFX8LCPHW2AE)