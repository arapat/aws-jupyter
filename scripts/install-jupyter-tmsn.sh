# Mount SSD
# ami-07ebfd5b3428b6f4d
killall jupyter-notebook
sleep 1
nohup jupyter notebook --no-browser --port=8888 < /dev/null > /dev/null 2>&1 &
URL=$(dig +short myip.opendns.com @resolver1.opendns.com)
sleep 2

echo
echo "The Jupyter Notebook is running on the cluster at the address below."
echo
echo "Open the following address using the browser on your computer"
echo
echo "  http"$(jupyter notebook list | grep -Po '(?<=http).*(?=::)' | sed "s/\/.*:/\/\/$URL:/")
echo
echo "(If the URL didn't show up, please wait a few seconds and try again.)"
echo