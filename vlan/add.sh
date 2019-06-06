#!/bin/bash
python print.py > 101
cat 101 | sed -n '/name/,/policy/{/policy/b;p}' > 102

cat 102 |grep name |awk '{print$3" "$4" "$5}' > 103
cat 102 |grep vlanId |awk '{print$3}' >104
cat 102 |grep vswitchName |awk '{print$3}' >105

paste 103 104 105 >106
#sed s/[[:space:]]//g 106 >107
sed 's/,\s*/, /g' 106 >107
rm 103 104 105 106 

sed 's/^/[/g' 107 >108
sed '1,$s/^/            /g' 108 > 103
rm 108 107
sed 's/..$//' 103 >104
sed 's/$/]/g' 104 >105
sed 's/$/,/g' 105 >106
rm 103 104 105
sed '$s/],/]/g' 106 > 103
sed "/Management/d" 103 >104
sed "/VMkernel/d" 104 >105
sed "/VM Network/d" 105 >107
sed '$s/],/]/g' 107 > 108
sed -i '109r108' addportgroup.py
rm 106 102 101 103 104 105 107 108
python addportgroup.py
