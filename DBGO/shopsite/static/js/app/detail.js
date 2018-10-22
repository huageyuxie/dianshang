/*********物品详情页的动画效果**********/
$(function(){
	
	/*控制左右按钮的显示与消失*/
	function btntoggle(){
		if(parseInt($(".good_img_list").css("left"))==0){
			$(".goodimg_listleft").css({"display":"none"});
			$(".goodimg_listright").css({"display":"block"});
		}else if(parseInt($(".good_img_list").css("left"))==($(".good_smallimg li").length-5)*-$imgWidth){
			$(".goodimg_listright").css({"display":"none"});
			$(".goodimg_listleft").css({"display":"block"});
		}else{
			$(".goodimg_listleft").css({"display":"block"});
			$(".goodimg_listright").css({"display":"block"});
		}
	}
	
	/*点击小图更换大图图片*/
	var $imgWidth=$(".good_img_list img").width();
	var $smallimgW=$(".good_smallimg_list li").outerWidth();
	
	//设置两倍的小图片，小图片的父级即ul设置为原来的两倍宽
	$(".good_smallimg_list").html($(".good_smallimg_list").html()+$(".good_smallimg_list").html());
	$(".good_smallimg_list").css({"width":$(".good_smallimg_list").width()+$(".good_smallimg_list").width()});
	$(".good_smallimg li").each(function(index,value){
		$(value).on("click",function(){
			$icurindex=$(this).index();
			if($(this).index()==4){
				$icurindex=0;
			}else if($(this).index()==5){
				$icurindex=1;
			}else if($(this).index()==6){
				$icurindex=2;
			}
			$(".good_img_list").css({"left":$icurindex*-$imgWidth});
			btntoggle();
		});	
	});
	
	
	btntoggle();

	
	/*点击左右按钮切换图片*/
	/*点击左边按钮*/
	$(".goodimg_listleft").on("click",function(){
		if(parseInt($(".good_img_list").css("left"))==0){
			$(".good_img_list").css({"left":0});
		}else{
			
			$(".good_img_list").css({"left":parseInt($(".good_img_list").css("left"))+$imgWidth});
			//用于获取当前下标  复制
			var index=parseInt($(".good_img_list").css("left"))/$imgWidth;
			//设置小图标的位置
			$(".good_smallimg_list").css({"left":(index*$smallimgW)});
		}
		btntoggle();
	});
	/*点击右边按钮*/
	$(".goodimg_listright").on("click",function(){
		if(parseInt($(".good_img_list").css("left"))==($(".good_smallimg li").length-5)*-$imgWidth){
			$(".goodimg_listright").css({"display":"none"});
		}else{
			$(".good_img_list").css({"left":parseInt($(".good_img_list").css("left"))-$imgWidth});
		}
		btntoggle();
	});
	
	/*遮罩层  动画效果,点击小图片切换大图片*/
	$(".select_img_list li").each(function(index,value){
		$(value).on("click",function(){
			$(".show_img img").attr({"src":"../img/show_img"+($(this).index()+1)+".jpg"});
		});
	});
	
	
	/*点击图片,遮罩层出来*/
	$(".good_img_list li").on("click",function(){
		$("#backgroundDiv").css({"display":"block"});
		$(".main_wraper").css({"display":"none"});
		$(window).scrollTop(0);
	});
	$(".divcloseimg").on("click",function(){
		$("#backgroundDiv").css({"display":"none"});
		$(".main_wraper").css({"display":"block"});
	});
	
	/*物品介绍第一部分右边的展开收缩活动效果*/
	$(".unfold_btn").on("click",function(){
		$(".good_activity2").slideToggle(400);
	});
	
	/*点击购物车加减按钮,确定购买数量*/
	
	$(".num_reduce").on("click",function(){
		$("#truenum").val($("#truenum").val()-1);
		if($("#truenum").val()<5){
			$(".num_add").removeClass("false_choose");
		}
		if($("#truenum").val()<1){
			$(".num_reduce").addClass("false_choose");
			$("#truenum").val("1");
		}
	});
	$(".num_add").on("click",function(){
		$("#truenum").val(parseInt($("#truenum").val())+1);
		if($("#truenum").val()>1){
			$(".num_reduce").removeClass("false_choose");
		}
		if($("#truenum").val()>5){
			$(".choose_explain").css({"display":"block"});
			$(".num_add").addClass("false_choose");
			$("#truenum").val("5");
			$(".choose_explain").html("您一次最多只能添加5件商品");
			setTimeout(function(){
				$(".choose_explain").css({"display":"none"});
			},1500);
		}
	});
	
	
	
	/*鼠标移上,提示信息出来*/
		$(".alert_tips").hover(
			
			function(){
				$(this).next().css({"display":"block"});
			},
			function(){
				$(this).next().css({"display":"none"});
			}
		);

	/***************设置倒计时、过期时间******************/
	function countDown(newdate){
		var date=new Date();
		var num=(newdate-date)/1000;
		var day=Math.floor(num/86400);
		var hours=Math.floor(num%86400/3600);
		var minutes=Math.floor(num%86400%3600/60);
		var seconds=Math.floor(num%60);
		$(".countdownD").html(two(day));
		$(".countdownH").html(two(hours));
		$(".countdownM").html(two(minutes));
		$(".countdownS").html(two(seconds));
	}
	function two(n){
		return n<=9?"0"+n:""+n;
	}
	newTime=new Date(2016,8,30,18,0,0);
	setInterval(function(){
		countDown(newTime);
	},1000);
	
	
	
})
