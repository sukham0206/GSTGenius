var row_counter = 1;

function add_row() {
  old_item_row_count = row_counter;
  row_counter++;

  $("#invoice-form-items-table-body >tr:last")
    .clone(true)
    .insertAfter("#invoice-form-items-table-body >tr:last");
  $("#invoice-form-items-table-body >tr:last input").val("");

  $("#invoice-form-items-table-body >tr:last td")[0].innerHTML =
    row_counter;
  update(
    $("#invoice-form-items-table-body input[name=invoice-qty]:last")
  );
}

function multi_rows() {
  $("#invoice-form-addrow").click(function (event) {
    event.preventDefault();
    add_row();
  });
  for (var i = 0; i < 4; i++) {
    add_row();
  }
}

function update_inv() {
  sum = 0;
  $("input[name=invoice-amt-without-gst]").each(function () {
    sum += parseFloat($(this).val());
  });
  $("input[name=invoice-total-amt-without-gst]").val(
    sum.toFixed(2)
  );

  sum_sgst = 0;
  $("input[name=invoice-amt-sgst]").each(function () {
    sum_sgst += parseFloat($(this).val());
  });
  $("input[name=invoice-total-amt-sgst]").val(sum_sgst.toFixed(2));

  sum_cgst = 0;
  $("input[name=invoice-amt-cgst]").each(function () {
    sum_cgst += parseFloat($(this).val());
  });
  $("input[name=invoice-total-amt-cgst]").val(sum_cgst.toFixed(2));

  sum_igst = 0;
  $("input[name=invoice-amt-igst]").each(function () {
    sum_igst += parseFloat($(this).val());
  });
  $("input[name=invoice-total-amt-igst]").val(sum_igst.toFixed(2));

  final_sum = 0;
  $("input[name=invoice-amt-with-gst]").each(function () {
    final_sum += parseFloat($(this).val());
  });
  $("input[name=invoice-total-amt-with-gst]").val(final_sum.toFixed(2));
}

function calc() {
  update(
    $("#invoice-form-items-table-body input[name=invoice-qty]:first")
  );
  $(
    "input[name=invoice-qty], input[name=invoice-gst-percentage], input[name=invoice-rate-with-gst]"
  ).change(function () {
    update($(this));
  });
}

function update(element) {
  var product = element
    .parent()
    .parent()
    .find("input[name=invoice-product]")
    .val();
  var qty = parseInt(
    element.parent().parent().find("input[name=invoice-qty]").val()
  );
  var rate_with_gst = parseFloat(
    element.parent().parent().find("input[name=invoice-rate-with-gst]").val()
  );
  var gst_percentage = parseFloat(
    element.parent().parent().find("input[name=invoice-gst-percentage]").val()
  );

  var rate_without_gst = (rate_with_gst * 100.0) / (100.0 + gst_percentage);
  var amt_without_gst = rate_without_gst * qty;

  var sgst;
  var cgst;
  var igst;
  if (product == "") {
    sgst = 0;
    cgst = 0;
    igst = 0;
    amt_without_gst = 0;
  } else {
    if ($("input[name=igstcheck]").is(":checked")) {
      sgst = 0;
      cgst = 0;
      igst = (amt_without_gst * gst_percentage) / 100;
    } else {
      sgst = (amt_without_gst * gst_percentage) / 200;
      cgst = (amt_without_gst * gst_percentage) / 200;
      igst = 0;
    }
  }
  var amt_with_gst = amt_without_gst + cgst + sgst + igst;

  element
    .parent()
    .parent()
    .find("input[name=invoice-rate-without-gst]")
    .val(rate_without_gst.toFixed(2));
  element
    .parent()
    .parent()
    .find("input[name=invoice-amt-without-gst]")
    .val(amt_without_gst.toFixed(2));
  element
    .parent()
    .parent()
    .find("input[name=invoice-amt-sgst]")
    .val(sgst.toFixed(2));
  element
    .parent()
    .parent()
    .find("input[name=invoice-amt-cgst]")
    .val(cgst.toFixed(2));
  element
    .parent()
    .parent()
    .find("input[name=invoice-amt-igst]")
    .val(igst.toFixed(2));
  element
    .parent()
    .parent()
    .find("input[name=invoice-amt-with-gst]")
    .val(amt_with_gst.toFixed(2));

  update_inv();
}

$(document).ready(function () {
  multi_rows();

  calc();

  $("input[name=igstcheck]").change(function () {
    $("input[name=invoice-qty]").each(function () {
      update($(this));
    });
  });

  $("#invoice-form")[0].hidden = false;
});
