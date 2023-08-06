Chào mừng bạn đã đến với bản demo Edu4All của dự án "Ánh sáng trong em"
Chúng mình là nhóm "Code đến hơi thở cuối cùng"
Sau đây sẽ là một số hướng dẫn để bạn có thể tải về và khởi chạy được trang web này

I) Tải code về máy:
Cách 1: Tải code về máy bằng git clone
	1.Tải git về máy (nếu chưa)
	2.Mở git bash tại thư mục hoặc vị trí bạn muốn tải về 

	3.Cài đặt cấu hình cho máy: (nếu chưa)
		-> example:	git config --global user.name "John Doe"
		-> example:	git config --global user.email johndoe@example.com

	4.Gõ lệnh 
		git clone https://github.com/ptyants/share-code-steam-hack.git

Cách 2: Tải tất cả code về theo cách thông thường

II) Khởi tạo môi trường và thư viên cần thiết:
* trong quá trình cài đặt và tải các gói khuyến kích sử dụng trên Command Prompt (CMD) dưới quyền admin
1. Tạo môi trường ảo cho python:
	On Windows, run:
		python -m venv tutorial-env

	-> example:  python -m venv venv

	On MacOS, run:	
		python3 -m venv .env
	
2. khởi chạy Environment:
	On Windows, run:
		tutorial-env\Scripts\activate.bat

	-> example: venv\Scripts\activate.bat

	On Unix or MacOS, run:
		source tutorial-env/bin/activate

   	Nếu gặp lỗi về "Execution Policies", chạy: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted sẽ cho phép máy có quyền chạy lệnh

3. Nhập các package:
		pip install -r requirements.txt

	Trong quá trình cài đặt của file requirements.txt có thể hơi lâu vì có những thư viện thừa mà tôi chưa thể xác định được
	Nên xin hãy chờ đợi trong ít phút

Nếu bạn tải và cài đặt đến giờ mà chưa gặp vấn đề gì thì xin chúc mừng bạn đặt hoàn thành !

Nếu bạn gặp lỗi về một vài thư viện không thể import được xin hỗ bổ sung nó sau

# --debug: Cập nhật lại ứng dụng mỗi khi có thay đổi
flask --debug run
# Có một số trường hợp sử dụng vscode báo Warning nhưng vẫn có thể khởi chạy chương trình khi gõ lệnh này trên thanh terminal: flask run


Tham khảo thêm ở: https://blogchiasekienthuc.com/lap-trinh/cai-dat-git-tren-windows-10.html (cách tải git về máy)
				  https://www.youtube.com/watch?v=N_tabayXkdI     (Cách clone dự án từ GitHub về máy)
		  		  https://www.youtube.com/watch?v=7EKM0V9FqUA	  (Clone dự án từ Repo Github về Git trong 1 câu lệnh)
                  https://docs.python.org/3/tutorial/venv.html    (cách tạo môi trường ảo cho máy)
			      https://t3h.com.vn/tin-tuc/trien-khai-ung-dung-vi-du-python-flask-bang-heroku  (cách tạo môi trường ảo cho máy)


III) Một số chú thích về việc vận hành web:
    - Các loại thẻ đã ghi trong file "tags list.txt" sẽ được hiển thị để người dùng (học viên và giáo viên) có thể chọn  
    - Nên bạn có thể thêm bớt các thẻ tag trong file "tags list.txt" để người dùng có thể thấy được những gì bạn muốn hướng đến
    - File "tags list.txt" sẽ hoạt động độc lập với dữ liệu chương trình nên việc bạn xóa thẻ tag chỉ có thể khiến cho người dùng sẽ không thể nhìn thấy thẻ tag đó để chọn nữa thôi
    - Chỉ khi người dùng submit các thẻ đã chọn một lần nữa sau khi xóa thẻ tag trong file "tags list.txt" thì lúc đó người dùng mới chính thức không thể thấy được các video của thẻ tag đó
    - Chạy file app.py để vận hành hệ thống

IV) Một số tài khoản mà bạn có thể trực tiếp trải nghiệm web mà không cần đăng ký:
1.	Role giáo viên: (gõ liền không cách)
		User_name: gv
		Email: gv@dds
		Password: gv

2. 	Role học viên: (gõ liền không cách)
(Nếu bạn muốn trải nghiệm như một học viên mới thì xin hãy tự tạo khoản riêng để trải nghiệm)

		User_name: Thế An
		Password: Thế An

		User_name: hs
		Email: hs@s
		Password: hs



Nếu bạn có thắc mắc hoặc những ý tưởng cải tiến bổ sung gì về trang web,
 gặp vấn đề trong việc tải xuống hoặc khởi chạy web mà chưa chỉnh sửa, xin hãy liên hệ gmail: phamtheants@gmail.com

Edu4All - Xin cảm ơn