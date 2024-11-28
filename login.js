// 登录常量
var LOGIN_USERNAME_ID = ".login-main .m-account #username";
var LOGIN_PASSWORD_ID = ".login-main .m-account #password";
var LOGIN_CAPTCHA_ID = ".login-main .m-account #captcha";
var LOGIN_ACCOUNT_ID = ".login-main .m-phone #username";
var LOGIN_DYNAMIC_ID = ".login-main .m-phone #dynamicCode";
var LOGIN_DYNAMIC_CAPTCHA_ID = ".login-main .m-phone #captcha";
var LOGIN_SUBMIT_ID = ".login-main #login_submit";
var QR_LOGIN_ENABLED = 0;
var DEFAULT_SALT = "rjBFAaHsNkKAhpoi";

var excludeRegular =
    window.excludeRegular === undefined
        ? "用户名包含特殊字符！"
        : excludeRegular;
var reg = window.reg === undefined ? "" : reg;
/**
 * 1. 加载的时候，根据情况判断是否显示验证码，如果需要，重新加载验证码
 * 2. 用户名失去焦点的时候，发请求校验需不需要验证码
 * 3. 如果需要验证码，显示验证码输入框，重新加载验证码
 * 4. 如果不需要验证码，清空验证码输入框，隐藏验证码区域
 * 5. 登录失败的时候，判断是否需要验证码，如果需要，重新验证码
 */
window.onload = function () {
    //图片轮播
    setMyInterval();
    //兼容IE
    // compliantIE();

    //实现多图轮播
    var gnum = 0;
    setInterval(function () {
        gnum++;
        if (gnum == 2) {
            gnum = 0;
        }
        $(".mainbg")
            .eq(gnum)
            .addClass("active")
            .siblings()
            .removeClass("active");
        // $(".dz_logo img").eq(gnum).addClass('active').siblings().removeClass('active');
    }, 8000);
    //
    var num = $(".dz_item").length;
    var initnum = 1;
    $("#pageTotal").text(num);
    $("#pageNum").text(initnum);
    $("#goPre").click(function () {
        if (initnum != 1) {
            initnum--;
            $("#pageNum").text(initnum);
            $(".remark_box").animate({ left: -630 * (initnum - 1) });
        }
    });
    $("#goNext").click(function () {
        console.log(111);
        if (initnum != num) {
            initnum++;
            $("#pageNum").text(initnum);
            $(".remark_box").animate({ left: -630 * (initnum - 1) });
        }
    });
    //处理url后面拼接service
    if (service && service != "") {
        //FORM表单
        utils.setUrlParam("pwdFromId", "?service", encodeURIComponent(service));
        utils.setUrlParam(
            "phoneFromId",
            "?service",
            encodeURIComponent(service)
        );
        utils.setUrlParam(
            "loginFromId",
            "?service",
            encodeURIComponent(service)
        );
        //兼容性登录
        utils.setUrlParam(
            "commonLoginA",
            "&service",
            encodeURIComponent(service)
        );
        //忘记密码帐号激活
        utils.setUrlParam(
            "retrievePassId",
            "?service",
            encodeURIComponent(service)
        );
        utils.setUrlParam(
            "activationAccountId",
            "?service",
            encodeURIComponent(service)
        );
        //联合登录
        utils.setUrlParam(
            "combinedLogin_a_weiBo",
            "&success",
            encodeURIComponent(service)
        );
        utils.setUrlParam(
            "combinedLogin_a_weiXin",
            "&success",
            encodeURIComponent(service)
        );
        utils.setUrlParam(
            "combinedLogin_a_qq",
            "&success",
            encodeURIComponent(service)
        );
        //联合认证插件化
        setUrlForSuccessByClass(service);
        //校外用户登录
        utils.setUrlParam(
            "outUserLoginA",
            "&service",
            encodeURIComponent(service)
        );
    }
    //页面登录方式设置
    showTabHeadAndDiv("", 0);
    //设置多语言下拉选项
    getLanguageSwitch();

    //点击二维码显示二维码
    $("#qrCodeA").click(function () {
        $("#qrCodeA").hide();
        $("#qrCodeB").show();
        $(".main").hide();
        $(".auth-qroce").show();
        QR_LOGIN_ENABLED = 1;
        getQrCode();
    });

    $("#qrCodeB").click(function () {
        $("#qrCodeA").show();
        $("#qrCodeB").hide();
        $(".main").show();
        $(".auth-qroce").hide();
        QR_LOGIN_ENABLED = 0;
        getQrCode();
    });

    //键盘Enter提交
    $("body").on("keyup", function (event) {
        if (event.keyCode == 13) {
            startLogin($(LOGIN_SUBMIT_ID));
        }
    });
};

//登录页选项卡展示
function showTabHeadAndDiv(loginType, operType) {
    QR_LOGIN_ENABLED = 0;
    var openFlag = window.localStorage.getItem("anonbiometricso");
    var fidoUserId = window.localStorage.getItem("anonbiometricsu");
    loginType = utils.isEmptyStr(loginType) ? cllt : loginType;
    //fido登录是否支持
    if (
        openFlag != "true" ||
        !openFlag ||
        !fidoUserId ||
        !fidoEnabled() ||
        !isDeviceBinded()
    ) {
        //排除手动url添加type
        if (type == "fidoLogin") {
            window.location.href = contextPath;
            return;
        }
        $("#fidoLoginSpan").remove();
    } else {
        $("#fidoLoginSpan").show();
    }
    //手机动态码登录是否支持
    if (is_dynamicLogin != "true" || !is_dynamicLogin) {
        //排除手动url添加type
        if (type == "dynamicLogin") {
            window.location.href = contextPath;
            return;
        }
        //不展示 删除span 及 样式调整
        $("#phoneLoginSpan").remove();
    } else {
        $("#phoneLoginSpan").show();
    }
    //关闭帐号密码登录
    if (
        window.is_userNameLogin != undefined &&
        window.is_userNameLogin != "true"
    ) {
        $("#pwdLoginSpan").remove();
    } else {
        $("#pwdLoginSpan").show();
    }
    // 先判断二维码登录是否开启
    $("#qrLoginSpan").show();
    // if (isQrLoginEnabled === "true") {
    //     //二维码扫码登录是否支持嵌入
    //     if (isQrLogin != "true" || !isQrLogin) {
    //         //排除手动url添加type
    //         if (loginType == 'qrLogin') {
    //             window.location.href = contextPath;
    //             return;
    //         }
    //         $("#qrCodeA").show();
    //         $("#qrLoginSpan").remove();
    //     } else {
    //         $("#qrLoginSpan").show();
    //         $("#qrCodeA").hide();
    //     }
    // } else {
    //     $("#qrLoginSpan").remove();
    //     $("#qrCodeA").hide();
    // }
    //设置登录方式标题长度样式
    // var spanNum = $(".tabHead").children("span").length;
    // var pwidth = ($(".tabHead").width() - 22 * spanNum) / spanNum;
    // $('.tabHead .loginFont_a').css("max-width", pwidth);
    var a =
        ($(".tabHead").width() *
            (100 / $(".tabHead").children("span").length)) /
        100;
    $(".tabHead span").css("width", a);
    //加载指定登录方式div
    $("#loginViewDiv").empty();
    $(".help, .help-inline").hide();
    $(".tabHead .tabHead-underline").css("display", "none");
    $(".tabHead").find("span").removeClass("selected_underline");
    if (
        (loginType == "" || !loginType) &&
        openFlag == "true" &&
        fidoUserId != "" &&
        fidoUserId &&
        fidoEnabled() &&
        isDeviceBinded()
    ) {
        //如果fido支持，fido登录页为默认
        $("#fidoLoginSpan .tabHead-underline").css("display", "block");
        $("#fidoLoginSpan").addClass("selected_underline");
        $("#loginViewDiv").html($("#fidoLoginDiv").html());
        $(".help, .help-inline").show();
    } else if (loginType == "fidoLogin" && fidoEnabled() && isDeviceBinded()) {
        //fido指纹认证登录
        $("#fidoLoginSpan .tabHead-underline").css("display", "block");
        $("#fidoLoginSpan").addClass("selected_underline");
        $("#loginViewDiv").html($("#fidoLoginDiv").html());
        $(".help, .help-inline").show();
    } else if (loginType == "qrLogin") {
        $("#qrLoginSpan .tabHead-underline").css("display", "block");
        $("#qrLoginSpan").addClass("selected_underline");
        $("#loginViewDiv").html($("#qrLoginDiv").html());
        $(".help").hide();
        //二维码登录
        QR_LOGIN_ENABLED = 1;
        //调用qrcode.js方法获取二维码
        getQrCode();
    } else if (loginType == "dynamicLogin") {
        //动态码登录
        $("#phoneLoginSpan .tabHead-underline").css("display", "block");
        $("#phoneLoginSpan").addClass("selected_underline");
        $("#loginViewDiv").html($("#phoneLoginDiv").html());
        $(".help").show();
        reloadCaptcha(true);
    } else if (
        window.is_userNameLogin != undefined &&
        window.is_userNameLogin != "true"
    ) {
        //动态码登录
        $("#phoneLoginSpan .tabHead-underline").css("display", "block");
        $("#phoneLoginSpan").addClass("selected_underline");
        $("#loginViewDiv").html($("#phoneLoginDiv").html());
        $(".help").show();
        reloadCaptcha(true);
    } else {
        //用户名密码登录
        $("#pwdLoginSpan .tabHead-underline").css("display", "block");
        $("#pwdLoginSpan").addClass("selected_underline");
        $("#loginViewDiv").html($("#pwdLoginDiv").html());
        $(".help").show();
        checkNeedCaptcha();
    }
    //输入框错误提示语清除
    flushItem(operType);
    //input禁止自动填入
    reloadInput();
    //切换主题色
    changeThemeColor();
}

function fidoEnabled() {
    //判断fido是否开启
    try {
        if (_fidoEnabled == undefined || _fidoEnabled == "true") {
            return true;
        }
    } catch (err) {
        console.log("捕获到异常：", err);
    }
    return false;
}

function startDynamicCode() {
    $(".login-main .loginFromClass .item-error-tip").empty();
    utils.cleanRequire($(".login-main .loginFromClass"), $("#showErrorTip"));
    if (
        utils.requireInput(
            $(LOGIN_ACCOUNT_ID),
            0,
            100,
            $("#nameErrorTip"),
            inputMobileTip,
            $(LOGIN_ACCOUNT_ID)
        )
    ) {
        return;
    }
    if (captchaSwitch == "2") {
        createSliderCaptcha();
    } else {
        getDynamicCode();
    }
}

function startLogin(that) {
    utils.disabledBtn(that, true);
    $(".login-main .loginFromClass .item-error-tip").empty();
    utils.cleanRequire($(".login-main .loginFromClass"), $("#showErrorTip"));
    if (checkForm()) {
        var cllt = $(".login-main #cllt").val();
        if (needCaptcha && captchaSwitch == "2" && cllt == "userNameLogin") {
            createSliderCaptcha();
            utils.disabledBtn(that, false);
        } else {
            $(".login-main .loginFromClass").submit();
        }
    } else {
        utils.disabledBtn(that, false);
    }
}

// 登录前校验
function checkForm() {
    var cllt = $(".login-main #cllt").val();
    if (cllt == "userNameLogin") {
        if (
            utils.requireInput(
                $(LOGIN_USERNAME_ID),
                0,
                100,
                $("#nameErrorTip"),
                inputUserNameTip,
                $(LOGIN_USERNAME_ID)
            ) ||
            utils.requireInput(
                $(LOGIN_PASSWORD_ID),
                0,
                32,
                $("#pwdErrorTip"),
                inputPasswordTip,
                $(LOGIN_PASSWORD_ID)
            )
        ) {
            return;
        }
        if (checkSpecificKey($(LOGIN_USERNAME_ID).val())) {
            return;
        }
        if (
            needCaptcha &&
            captchaSwitch == "1" &&
            utils.requireInput(
                $(LOGIN_CAPTCHA_ID),
                0,
                10,
                $("#captchaErrorTip"),
                inputCodeTip,
                $(LOGIN_CAPTCHA_ID)
            )
        ) {
            return;
        }
        $("#saltPassword").val(
            encryptPassword(
                $(LOGIN_PASSWORD_ID).val(),
                $("#pwdEncryptSalt").val()
            )
        );
        $(LOGIN_PASSWORD_ID).attr("disabled", "disabled");
    } else if (cllt == "dynamicLogin") {
        if (
            utils.requireInput(
                $(LOGIN_ACCOUNT_ID),
                0,
                100,
                $("#nameErrorTip"),
                inputMobileTip,
                $(LOGIN_ACCOUNT_ID)
            ) ||
            utils.requireInput(
                $(LOGIN_DYNAMIC_ID),
                0,
                100,
                $("#dynamicErrorTip"),
                inputDynamicTip,
                $(LOGIN_DYNAMIC_ID)
            )
        ) {
            return;
        }
        if (checkSpecificKey($(LOGIN_ACCOUNT_ID).val())) {
            return;
        }
    }
    return true;
}
function checkUserCaptcha() {
    checkSpecificKey($(LOGIN_USERNAME_ID).val());
    checkNeedCaptcha();
}

//校验是否需要验证码
function checkNeedCaptcha() {
    //判断验证码是否一直显示
    if (_badCredentialsCount && _badCredentialsCount == 0) {
        reloadCaptcha(true);
        return;
    }
    var username = $(LOGIN_USERNAME_ID).val().trim();
    if (utils.isEmptyStr(username)) {
        reloadCaptcha(false);
        return;
    }
    $.ajax(contextPath + "/checkNeedCaptcha.htl", {
        data: { username: username },
        cache: false,
        dataType: "json",
        success: function (data) {
            if (data.isNeed) {
                needCaptcha = true;
            } else {
                needCaptcha = false;
            }
            reloadCaptcha(needCaptcha);
        },
    });
}

//重新载入验证码
function reloadCaptcha(isNeed) {
    needCaptcha = isNeed;
    if (isNeed && captchaSwitch == "1") {
        $(".login-main #captchaDiv").show();
        $(".login-main #captchaTitle").show();
        $(".login-main #captchaImg").attr(
            "src",
            contextPath + "/getCaptcha.htl?" + new Date().getTime()
        );
        $(".container-ge .ge-btn").css("margin-top", "2px");
    } else {
        // 如果不需要验证码，那么清空
        $(".login-main #captcha").val("");
        $(".login-main #captchaDiv").hide();
        $(".login-main #captchaTitle").hide();
        $(".container-ge .ge-btn").css("margin-top", "");
    }
}

//发送动态码
function getDynamicCode() {
    if (
        utils.requireInput(
            $(LOGIN_ACCOUNT_ID),
            0,
            100,
            $("#nameErrorTip"),
            inputMobileTip,
            $(LOGIN_ACCOUNT_ID)
        )
    ) {
        return;
    }
    if (
        captchaSwitch == "1" &&
        utils.requireInput(
            $(LOGIN_DYNAMIC_CAPTCHA_ID),
            0,
            100,
            $("#captchaErrorTip"),
            inputCodeTip,
            $(LOGIN_DYNAMIC_CAPTCHA_ID)
        )
    ) {
        return;
    }
    var mobile = encryptPassword($(LOGIN_ACCOUNT_ID).val(), DEFAULT_SALT);
    var dynamicCaptcha = $(LOGIN_DYNAMIC_CAPTCHA_ID).val();
    $.ajax(contextPath + "/dynamicCode/getDynamicCode.htl", {
        data: { mobile: mobile, captcha: dynamicCaptcha },
        cache: false,
        dataType: "json",
        type: "POST",
        success: function (data) {
            var code = data.code;
            //var mobile = data.mobile;
            if (code == "error") {
                $(LOGIN_DYNAMIC_CAPTCHA_ID).val("");
                utils.showMsg($(".login-main #showErrorTip"), data.message);
                reloadCaptcha(true);
            } else if (code == "captchaError") {
                $(LOGIN_DYNAMIC_CAPTCHA_ID).val("");
                utils.showMsg($(".login-main #showErrorTip"), data.message);
                reloadCaptcha(true);
            } else if (code == "timeExpire") {
                $(LOGIN_DYNAMIC_CAPTCHA_ID).val("");
                if (!utils.isEmptyStr(data.time)) {
                    getTimes(data.time);
                }
                utils.showMsg($(".login-main #showErrorTip"), data.message);
            } else if (code == "success") {
                $(".login-main #showErrorTip").empty();
                utils.showMsg($(".login-main #showWarnTip"), data.message, 0);
                getTimes(data.intervalTime);
            }
        },
    });
}

function setUrlForSuccessByClass(service) {
    var loginPlugins = $(".item .combinedLoginPlugin");
    if (loginPlugins) {
        loginPlugins.each(function () {
            $(this).attr(
                "href",
                $(this).attr("href") + "&success=" + encodeURIComponent(service)
            );
        });
    }
    var idsUnions = $(".ids-union-a");
    if (idsUnions) {
        idsUnions.each(function () {
            $(this).attr(
                "href",
                $(this).attr("href") + "&success=" + encodeURIComponent(service)
            );
        });
    }
}

//动态码倒计时
function getTimes(time) {
    if (time == 0) {
        reloadCaptcha(true);
        time = 120;
        $(".login-main .get-code").show();
        $(".login-main .get-code-tip").hide();
        return;
    } else {
        time--;
        $(".login-main .getCodeText").text(time + "S");
        $(".login-main .get-code").hide();
        $(".login-main .get-code-tip").show();
    }
    setTimeout(function () {
        getTimes(time);
    }, 1000);
}

//加载滑块验证码
function createSliderCaptcha() {
    $.ajax({
        url: contextPath + "/common/toSliderCaptcha.htl",
        type: "get",
        data: {},
        success: function (data) {
            $(".login-main #captchaDiv").hide();
            $(".login-main #captchaTitle").hide();
            $("#sliderCaptchaDiv").html(data);
        },
    });
}

//用户名校验特殊字符
function checkSpecificKey(input) {
    if (reg && reg != "") {
        var pattern = new RegExp(reg);
        if (pattern.test(input)) {
            $(".login-main #showErrorTip").text(excludeRegular);
            return true;
        } else {
            $(".login-main #showErrorTip").text("");
            return false;
        }
    }
    return false;
}

function setMyInterval() {
    setInterval(function () {
        //实现多图轮播切换
        $(".content-bg").each(function () {
            if (
                $(this).attr("src") == $(".swiper-slide-active img").attr("src")
            ) {
                $(this)
                    .addClass("active")
                    .siblings(".content-bg")
                    .removeClass("active");
            }
        });
        //二维码提示语
        if (
            $(".auth-qroce").css("display") != "none" &&
            $("#qr_invalid").length > 0
        ) {
            if ($("#qr_invalid").css("display") != "none") {
                $(".qrcode_tip").text(qrInvalidTip);
            } else {
                $(".qrcode_tip").text(qrLoginTip);
            }
        }
    }, 500);
}
//多语言下拉
function getLanguageSwitch() {
    var locale = utils.getCookie(
        "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE"
    );
    $.ajax({
        type: "POST",
        url: contextPath + "/common/getLanguageTypes.htl",
        dataType: "json",
        data: {},
        async: false,
        success: function (data) {
            $("#language_switch").empty();
            data.languageTypeList.forEach(function (type) {
                if (locale == type.languageKey) {
                    $("#language_switch_name").text(type.languageName);
                }
                $("#language_switch").append(
                    "<li class='text_ellipsis' onclick='changeLanguageSwitch(\"" +
                        type.languageKey +
                        "\")'>" +
                        type.languageName +
                        "</li>"
                );
            });
        },
    });
}

function changeLanguageSwitch(locale) {
    var cookieLocale = utils.getCookie(
        "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE"
    );
    if (locale && cookieLocale && locale != cookieLocale) {
        utils.setCookie(
            "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE",
            locale
        );
        window.location.reload();
    }
}

function flushItem(operType) {
    if (operType == 1) {
        utils.cleanRequire(
            $(".login-main .loginFromClass"),
            $("#showErrorTip")
        );
        $("input[type=text]").val("");
    }
    $(".login-main .loginFromClass .item-error-tip").empty();
    //重新输入清除错误提示语
    $("input").keyup(function () {
        utils.cleanRequire($(this).parent(), $("#showErrorTip"));
        $(this).siblings(".item-error-tip").empty();
    });
    //隐藏显示密码
    $(".login-main .ge-input-eye").click(function () {
        if ($(this).hasClass("eye-hide")) {
            $(this).removeClass("eye-hide").addClass("eye-show");
            $("#password").prop("type", "text");
        } else {
            $(this).removeClass("eye-show").addClass("eye-hide");
            $("#password").prop("type", "password");
        }
    });
    //元素hover提示语
    $(".item")
        .mouseover(function () {
            $(this).children(".item-show").show();
            $(this).children(".mobile-item-show").show();
            $(this).find(".g-switch-arrow").css("transform", "rotate(90deg)");
            $(this)
                .children(".item-show")
                .css(
                    "left",
                    -(
                        ($(this).children(".item-show").outerWidth() -
                            $(this).outerWidth()) /
                        2
                    )
                );
        })
        .mouseout(function () {
            $(this).children(".item-show").hide();
            $(this).children(".mobile-item-show").hide();
            $(this).find(".g-switch-arrow").css("transform", "");
        });
}

//兼容IE设置登录页居中
function compliantIE() {
    if (!!window.ActiveXObject || "ActiveXObject" in window) {
        var calPaddingTop = function () {
            var height = document.documentElement.clientHeight;
            if (height > 744) {
                $(".auth_page_content").css(
                    "padding-top",
                    (height - 744) / 2 + "px"
                );
            } else {
                $(".auth_page_content").css("padding-top", 0);
            }
        };
        calPaddingTop();
        $(window).resize(function () {
            calPaddingTop();
        });
    }
}
//切换主题色
function changeThemeColor() {
    var themeColor = jsonObject.pcThemeColor;
    if (utils.isNotEmptyStr(themeColor)) {
        //css变量设置方式(IE不兼容)
        $("body").css("--theme-color", themeColor);
        //js方式
        $(".tabHead").find(".loginFont_a").removeClass("change-color");
        $(".tabHead").find(".selected_underline a").addClass("change-color");
        $(".login-main .change-input-color").hover(
            function () {
                $(this).addClass("change-bd-color");
            },
            function () {
                $(this).removeClass("change-bd-color");
            }
        );
        $(".activation-account,.fo-password,.fetch-online").hover(
            function () {
                $(this).addClass("change-color");
            },
            function () {
                $(this).removeClass("change-color");
            }
        );
        $(".item-img")
            .mouseover(function () {
                $(this).addClass("change-bg-color");
                $(this).css("color", "#FFFFFF");
            })
            .mouseout(function () {
                $(this).removeClass("change-bg-color");
                $(this).css("color", "#4E5969");
            });
    }
}
