# weibo-prize
微博的转发抽奖脚本,配合crontab使用.

效果如图:

![微博图片](test.jpg)

注意点: 从mobile 界面获取用户的相关信息: container id 等, 而从 pc端作模拟登陆和请求转发

mid 是微博的id, reason是转发附加信息, 而username, password 直接填写就好

没有做转发次数测试, 但目前一天两条不会被封.
