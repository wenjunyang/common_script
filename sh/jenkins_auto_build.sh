zip_name="upload.zip"
#打包
zip -q -r ${zip_name} ${path}

#上传azkaban
#1. 身份验证
auth_result=`curl -k -X POST --data "action=login&username=${azkaban_username}&password=${azkaban_password}" ${host}`
session_id=${auth_result:44:36}

upload_result=`curl -k -i -H "Content-Type: multipart/mixed" -X POST --form "session.id=${session_id}" --form "ajax=upload" --form "file=@${zip_name};type=application/zip" --form "project=${project_name}" ${host}/manager`

#删除临时文件
rm $zip_name

echo "上传结果：$upload_result"

if [[ `echo $upload_result | grep "projectId"` != "" && `echo $upload_result | grep "version"` != "" ]]; then
    echo "部署成功"
    exit 0
else
    echo "部署失败"
    exit 1
fi  
