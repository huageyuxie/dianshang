$(document).ready(function() {
    var regUser = /^\w{6,18}$/,
        regPsw = /^[a-z0-9]{6,12}$/i;
        // regMail = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
    var $userErrorInfo = $('.setNumber-tishi1'),
        $pswErrorInfo = $('.setNumber-tishi2'),
        $repswErrorInfo = $('.setNumber-tishi3');
        // $codeErrorInfo = $('.setNumber-tishi4');
        // $mailErrorInfo = $('.setNumber-tishi4');
    var $user = $("input[name='username']"),
        $psw = $("input[name='password']"),
        $repsw = $("input[name='confirm_pwd']"),
        // $code = $("input[name='code']"),
        // $mail = $("input[name='mail']"),
        $submitBtn = $("input[type='submit']");
    //校验用户名
    $user.on('blur', function (e) {
        var userFlag = regUser.test($(this).val());
        console.log($(this).val());
        if (userFlag) {
            $userErrorInfo.html("用户名长度正确(6-18位)");
        }else{
            $userErrorInfo.html("用户名长度不正确且不能包含中文");
        }
    });
    //校验密码
    $psw.on('blur', function (e) {
        var pswFlag = regPsw.test($(this).val());
        if (pswFlag) {
            $pswErrorInfo.html("");
        }else{
            $pswErrorInfo.html("密码格式不正确");
        }
    });
    //校验确认密码
    $repsw.on('blur', function (e) {
        var repswVal = $(this).val(),
            pswVal = $psw.val();
        var repswFlag = (repswVal === pswVal);
        if (!repswFlag){
            $repswErrorInfo.html("<p color='red'>两次密码输入不一致</p>");
        }else{
            $repswErrorInfo.html("两次密码输入一致");
        }
    });

    // //校验邮箱
    // $mail.on('blur', function (e) {
    //     var mailFlag = regMail.test($(this).val());
    //     checkVal(mailFlag, $(this), $mailErrorInfo);
    // });
    //点击提交按钮
    $submitBtn.on('click', function (e) {
        console.log('点击提交按钮');
        var userFlag = regUser.test($user.val()),
            pswFlag = regPsw.test($psw.val()),
            repswFlag = ($repsw.val() === $psw.val());
            // mailFlag = regMail.test($mail.val());
        if (userFlag && pswFlag && repswFlag) {
            $('.setNumberbtn').submit();
        } else {
            e.preventDefault();
        }
    });
});


function change_code() {
    document.getElementById("code-img").src="/shopsite/code?id="+ Math.random()
}
