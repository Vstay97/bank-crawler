$(".yhks_article_btn").click(function () {
    if ($(".zhezhao").is(":hidden")) {
    $(".zhezhao").show()
    } else{
      $(".zhezhao").hide()
    }
  })
  $(".yhzptc_close").click(function () {
    $(".zhezhao").hide()
  })