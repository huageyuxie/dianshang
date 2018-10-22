$(function(){

	//******************************************网站首页特效*******************************************
	
	/*********网页右侧侧边栏***********/
	
	$(window).on("scroll",function(){
		if($(window).scrollTop()<480){
			$("#content").css({"margin-top":-($(window).scrollTop()+100)});
		}else if($(window).scrollTop()>=800){
			$(".clickOn").css({"display":"block"});
		}else{
			$(".clickOn").css({"display":"none"});
		}
	});
	
	$(".clickOn a").on("click",function(){
		$(window).scrollTop(0);
		$(".clickOn").css({"display":"none"});
	});
	
	
	/********************头部部分,鼠标滑动到"手机版",二维码出现******************/
	/*var $quickAccessList=*/$(".quick_access_right_list").find("a").hover(
		function(){
			$(this).next().css({"display":"block"});
		},
		function(){
			$(this).next().css({"display":"none"});
		}
	);
	
	
	/*******************首页网站导航---鼠标浮上导航菜单出现*********************/
	var $navLeftList=$("#nav_left .nav_left_list");
	$navLeftList.hover(
		function(){
			$(this).find("div").css({"display":"block"});
		},
		function(){
			$(this).find("div").css({"display":"none"});
		}
	);
	
	/**********鼠标悬浮在购物袋上,隐藏购物车的商品显示*****************/
	$("#nav_right").hover(
		function(){
			$(this).find(".nav_shopping_bag").stop(true,false).delay(500).slideDown(400);
		},
		function(){
			$(this).find(".nav_shopping_bag").stop(true,false).delay(500).slideUp(300);
		}
	);
		//点击close按钮关闭购物显示
		var $shopCLoseButton=$(".nav_button_close");
		$shopCLoseButton.on("click",function(){
			$(this).parent().parent().css({"display":"none"});
		});
	//菜单吸顶效果
	$(function() {
	  	$(function() {
	  		$("#nav_container").stickUp();
	  	});
	 });
	 
	/***主内容区的轮播图***/
	var timer = null;
	timer=setInterval(auto,2300);
	
		//点击右按钮
	var icurindex = 1;
	$(".page_right").on("click",function(){
		if(icurindex>=3){
			icurindex=1;
			$(".index_turn").css({left:-320});
		}
		icurindex++;
		$(".index_turn").stop(true,false).animate({left:(icurindex*-320)},500);
		red();
	});
	//点击左按钮
	$(".page_left").on("click",function(){
		if(icurindex<1){
			icurindex=2;
			$(".index_turn").css({left:-640});
		}
		icurindex--;
		$(".index_turn").stop(true,false).animate({left:(icurindex*-320)},500);
		red();
	});
	
	
	//点击下方按钮切换图片
	$(".pageBtn a").each(function(index,value){
		$(value).on("click",function(){
			icurindex=$(this).index()+1;
			$(".pageBtn a").removeClass("active");
			$(this).addClass("active");
			$(".index_turn").stop(true,false).animate({left:(icurindex*-320)},500);
		});
	});
	function red(){
		$(".pageBtn a").removeClass("active");
		if(icurindex==0||icurindex==2){
			$(".pageBtn a").eq(1).addClass("active");
		}else if(icurindex==1||icurindex==3){
			$(".pageBtn a").eq(0).addClass("active");
		}
	}
	
	/*自动轮播效果*/
	function auto(){
		if(icurindex>=3){
			icurindex=1;
			$(".index_turn").css({left:-320});
		}
		icurindex++;
		$(".index_turn").stop(true,false).animate({left:(icurindex*-320)},500);
		red();
	}
	
	$(".today_new_right").hover(
		function(){
			clearInterval(timer);
		},
		function(){
			timer=setInterval(auto,2300);
		}
	);
	
	/***主内容区的轮播图  end***/
	
	/*******************鼠标悬浮在图片上，图片放大*********************/
	$(".content_main_img").hover(
		function(){
			$(this).find(".content_main_goods").css({"display":"block"});
			$(this).first().find("img").addClass("greyscale");
			$(this).first().find("img").stop(true,false).animate({"width":"350px","height":"210px","left":"-15px","top":"-10px"},400);
		},
		function(){
			$(this).find(".content_main_goods").css({"display":"none"});
			$(this).first().find("img").removeClass("greyscale");
			$(this).first().find("img").stop(true,false).animate({"width":"318px","height":"191px","left":0,"top":0},400);
		}
	);
	
	
	/***即将开始的活动商品     鼠标移上遮罩层出来,点击订阅按钮可以订阅****/
	$(".activity_brand_block").each(function(index, value) {
		$(value).hover(
			function () {
				$(this).find(".activity_brand_mask").css({"display":"block"});
				$(this).find(".activity_brand_take").css({"display":"block"});
				$(this).has(".activity_brand_take").find(".take2").on("mousedown",function(event){
					event.stopPropagation();
					if($(this).html()=="订阅"){
							$(this).html("取消");
							$(this).css({"background":"#999","width":"50%"});
							$(this).siblings(".take1").css({"width":"50%"});
							$(this).siblings(".spacing").css({"display":"none"});
							$(this).parent().parent().prev().find(".activity_take_chose").html("已选择");
					}else{				
							$(this).html("订阅");
							$(this).css({"background":"none","width":"45%"});
							$(this).siblings(".take1").css({"width":"45%"});
							$(this).siblings(".spacing").css({"display":"block"});
							$(this).parent().parent().prev().find(".activity_take_chose").html("");
					}
					
				});
			},
			function () {
				$(this).has(".activity_brand_take").find(".take2").off("mousedown");
				$(this).find(".activity_brand_mask").css({"display":"none"});
				$(this).find(".activity_brand_take").css({"display":"none"});
			}
		);
	});

	/***即将开始的活动商品   点击时间可以切换查看不同时间折扣的商品 */
	$(".activitiesList_day li").each(function(index,value){
		$(value).on("click",function(){
			$(this).siblings().removeClass("active");
			$(this).addClass("active");
			$(".activity_brand").css({"display":"none"});
			$(".activity_brand").eq($(this).index()).css({"display":"block"});
		});
	});
	
	
})
