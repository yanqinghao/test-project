wget -O trackers_all.txt https://ngosang.github.io/trackerslist/trackers_all.txt
wget -O trackers_all_ip.txt https://ngosang.github.io/trackerslist/trackers_all_ip.txt
trackersList="Bittorrent\\\TrackersList="
while IFS= read -r line; do
    if [ -n "$line" ]; then
        trackersList="${trackersList}${line}\\\n"
    fi
done < trackers_all.txt
while IFS= read -r line; do
    if [ -n "$line" ]; then
        trackersList="${trackersList}${line}\\\n"
    fi
done < trackers_all_ip.txt
trackersListFormat=$(echo "$trackersList" | sed 's/\//\\\//g')
sed -i "s/Bittorrent\\\TrackersList=.*/${trackersListFormat}/" qBittorrent.conf
rm trackers_all.txt trackers_all_ip.txt
