$(function(){
	
	/*******************添加购物车部分*************************/
	
// 创建购物车
		$(window).on("load", function () {
			loadCart();
		});


		// 加载购物车中的商品
		function loadCart() {
			var carts = new CartHelper().Read();// 读取购物车中的数据
			$(".inner_have").remove();
			// 加载到页面上
			/******************* 加载购买商品信息 BEGIN***********************/
			$.each(carts.Items, function(index,cartItem) {

				updateCartPage(cartItem.Id, cartItem.Name, cartItem.Count, cartItem.Price, cartItem.imgPath);
			});
			/******************* 加载购买商品信息 END***********************/



		}



		//向购物车中添加数据
		$("#buy").on("click",function(){

			// 获取商品id
			var id = $(this).attr("data-id");
			// 获取图片路径
			var  imgPath = $(this).parents(".main1_inner_right").find("#data-src").attr("src");
			// 获取名称
			var goodsName = $(this).parents(".main1_inner_right").find(".main_right_tit").text()+"##"+$(this).parents(".main1_inner_right").find(".good_name h2").text();
			// 获取单价
			var price = $(this).parents(".main1_inner_right").find(".icurprice2").text();
			// 获取购买数量
			var count = $(this).parents(".main1_inner_right").find("#truenum").val();

			var $count1 = parseInt($(".goodsCount").html());

			if($count1+parseInt(count)>5){
				$(".choose_explain").css({"display":"block"});
				$(".choose_explain").html("您一次最多只能添加5件商品");
				setTimeout(function(){
					$(".choose_explain").css({"display":"none"});
				},1500);
				return false;
			}

			// 写购物车到cookie中
			new CartHelper().Add(id, goodsName, count, price, imgPath);

			// 加载购物车中的数据
				loadCart();//头部的购物袋中需要!!!

			$(".nav_shopping_bag").css({"display":"block"});
			setTimeout(function(){
					$(".nav_shopping_bag").slideUp(300);
			},1500);
		});

		/********************** 更新页面 ************************/
		function updateCartPage(id, goodsName, count, price, imgPath) {
			if(id){
				$(".inner_none").css({"display":"none"});
			}
			/*取goodsName的内容部分*/
			var $nameCon=goodsName.split("##");

		//创建总的div与里面的三个小部分
			var $inner = $("<div>");
			$inner.addClass("inner_have");
			//创建第一小部分的内容
			var $proCon = $("<div>");   //第一小部分的外部
			$proCon.addClass("my_product_container");
				$inner.append($proCon);
			var $product = $("<div>");
			$product.addClass("my_product");
			$product.attr({"data-id":id});
				$proCon.append($product);

			var $proImg = $("<a>");
			$proImg.addClass("my_product_img");
			$proImg.attr({href:"javascript:;"});
				$product.append($proImg);
			var $img = $("<img>");
			$img.attr({src:""+imgPath+"" ,title:$nameCon[1],alt:$nameCon[1]});
				$proImg.append($img);

			var $proDel = $("<a>");
			$proDel.addClass("my_product_delete");
			$proDel.attr({href:"javascript:;"});
			$proDel.html("删除");
				$product.append($proDel);
			var $aUl = $("<ul>");
				$product.append($aUl);
			var $lio = $("<li>");
			var $lioA = $("<a>");
			$lioA.attr({href:"javascript:;"});
			$lioA.html($nameCon[1]);
				$lio.append($lioA);
				$aUl.append($lio);
			var $lit = $("<li>");
				$aUl.append($lit);
			var $litr = $("<li>");
			var $spant = $("<span>");
			$spant.html("￥"+price);
				$litr.append($spant);
			var $span = $("<span>");
			$span.text(" x ");
				$litr.prepend($span);
			var $spano = $("<span>");
			$spano.html(count);
				$litr.prepend($spano);
				$aUl.append($litr);

			//创建第二小部分的内容
			var $subTotal = $("<div>");
			$subTotal.addClass("subtotal");
			$subTotal.html("购物袋小计");
			var $subSpan   = $("<span>");
			$subSpan.attr({style:"margin-right:15px;"});
			$subSpan.html("￥"+count * price);
				$subTotal.append($subSpan);
				$inner.append($subTotal);


			//创建第三小部分的内容
			var $proBtn = $("<a>");
			$proBtn.html("结算");
			$proBtn.attr({href:"shopbag.html"});
			$proBtn.addClass("my_product_button");
				$inner.append($proBtn);

			$(".nav_shopping_bag").append($inner);

			$(".goodsCount").html(count);
			$(".goodsprice").html("￥"+count * price);

		}
		/********************** 更新页面 ************************/


		/*移除购物袋中的物品*/
		$(".nav_shopping_bag").on("click", ".my_product_delete",function(){
			new CartHelper().Del($(this).parent().attr("data-id"));
			loadCart();
			if($(".nav_shopping_bag").children(".inner_have").size() <= 0){
				$(".inner_none").css({"display":"block"});
				$(".nav_shopping_bag").css({"height":"auto"});
				$(".goodsCount").html(0);
				$(".goodsprice").html("￥"+"0.00");
				setTimeout(function(){
					$(".nav_shopping_bag").slideUp(300);
				},1500);
			}
		});



	
	
	
	
})
