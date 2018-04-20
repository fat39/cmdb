/**
 * Created by Administrator on 2017/8/2.
 */
(function (jq) {
    var CREATE_SEARCH_CONDITION = true;
    var GLOBAL_DICT = {};
    /*
    {
        'device_type_choices': (
                                    (1, '服务器'),
                                    (2, '交换机'),
                                    (3, '防火墙'),
                                )
        'device_status_choices': (
                                    (1, '上架'),
                                    (2, '在线'),
                                    (3, '离线'),
                                    (4, '下架'),
                                )
    }
     */

    // 为字符串创建format方法，用于字符串格式化
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    function getSearchCondition(){
        var condition = {};
        $('.search-list').find('input[type="text"],select').each(function(){

            /* 获取所有搜索条件 */
            var name = $(this).attr('name');
            var value = $(this).val();
            if(condition[name]){
                condition[name].push(value);
            }else{
                condition[name] = [value];
            }

        });
        return condition;
    }

    // function initial(url) {
    function initial(url,current_page=1) {
        // 执行一个函数, 获取当前搜索条件
        var searchCondition = getSearchCondition();
        $.ajax({
            url: url,
            type: 'GET',  // 获取数据
            // data: {condition: JSON.stringify(searchCondition)},
            data: {condition: JSON.stringify(searchCondition),current_page:current_page},
            dataType: 'JSON',
            success: function (arg) {
                $.each(arg.global_dict,function(k,v){
                     GLOBAL_DICT[k] = v
                });

                initTableHeader(arg.table_config);
                initTableBody(arg.server_list, arg.table_config);
                initSearch(arg.search_config);
                initPager(url,arg.pager.current_page,arg.pager.page_count);
            }
        })
    }


    function initPager(url,current_page,page_count){
        $('.M-box3').pagination({
            pageCount: page_count,
            jump: true,
            coping: true,
            homePage: '首页',
            endPage: '末页',
            prevContent: '上页',
            nextContent: '下页',
            current:current_page,
            callback: function (api) {
                console.log(api.getCurrent());
                api.setPageCount(page_count);
                initial(url,api.getCurrent())
            }
        });
    }


    /*
    初始化搜索条件
     */
    function initSearch(searchConfig){
        if(searchConfig && CREATE_SEARCH_CONDITION){
            CREATE_SEARCH_CONDITION = false;
            // 找打searchArea ul，
            $.each(searchConfig,function(k,v){
                var li = document.createElement('li');
                $(li).attr('search_type', v.search_type);
                $(li).attr('name', v.name);
                if(v.search_type == 'select'){
                     $(li).attr('global_name', v.global_name);
                }

                var a = document.createElement('a');
                a.innerHTML = v.text;
                $(li).append(a);
                $('.searchArea ul').append(li);
            });

            // 初始化默认搜索条件
            // searchConfig[0],进行初始化
            // 初始化默认选中值
            $('.search-item .searchDefault').text(searchConfig[0].text);
            if(searchConfig[0].search_type == 'select'){
                var sel = document.createElement('select');
                $(sel).attr('class','form-control');
                $.each(GLOBAL_DICT[searchConfig[0].global_name],function(k,v){
                    var op = document.createElement('option');
                    $(op).text(v[1]);
                    $(op).val(v[0]);
                    $(sel).append(op)
                });
                $('.input-group').append(sel);
            }else{
                // <input type="text" class="form-control" aria-label="...">
                var inp = document.createElement('input');
                $(inp).attr('name',searchConfig[0].name);
                $(inp).attr('type','text');
                $(inp).attr('class','form-control');
                $('.input-group').append(inp);
            }


        }
    }

    function initTableHeader(tableConfig) {
        /*
         [
         {'q':'id','title':'ID'},
         {'q':'hostname','title':'主机名'},
         ]
         */
        $('#tbHead').empty();
        var tr = document.createElement('tr');
        $.each(tableConfig, function (k, v) {
            if (v.display) {
                var tag = document.createElement('th');
                tag.innerHTML = v.title;
                $(tr).append(tag);
            }
        });
        $('#tbHead').append(tr);
    }

    function initTableBody(serverList, tableConfig) {
        /*
         serverList = [
         {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-},
         {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-},
         {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-},
         {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-},
         ]
         */
        $('#tbBody').empty();
        $.each(serverList, function (k, row) {
            // row: {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-}
            /*
             <tr>
             <td>id</td>
             <td>hostn</td>
             <td>create</td>
             </tr>
             */
            var tr = document.createElement('tr');
            tr.setAttribute('nid',row.id);
            $.each(tableConfig, function (kk, rrow) {
                // kk: 1  rrow:{'q':'id','title':'ID'},         // rrow.q = "id"
                // kk: .  rrow:{'q':'hostname','title':'主机名'},// rrow.q = "hostname"
                // kk: .  rrow:{'q':'create_at','title':'创建时间'}, // rrow.q = "create_at"
                if (rrow.display) {
                    var td = document.createElement('td');

                    /* 在td标签中添加内容 */
                    var newKwargs = {}; // {'n1':'1','n2':'123'}
                    $.each(rrow.text.kwargs, function (kkk, vvv) {
                        var av = vvv;
                        if(vvv.substring(0,2) == '@@'){
                            var global_dict_key = vvv.substring(2,vvv.length);
                            var nid = row[rrow.q];
                            $.each(GLOBAL_DICT[global_dict_key],function(gk,gv){
                                if(gv[0] == nid){
                                    av = gv[1];
                                }
                            })
                        }
                        else if (vvv[0] == '@') {
                            av = row[vvv.substring(1, vvv.length)];
                        }
                        newKwargs[kkk] = av;
                    });
                    var newText = rrow.text.tpl.format(newKwargs);
                    td.innerHTML = newText;

                    /* 在td标签中添加属性 */
                    $.each(rrow.attrs,function(atkey,atval){
                        // 如果@
                        if (atval[0] == '@') {
                            td.setAttribute(atkey, row[atval.substring(1, atval.length)]);
                        }else{
                            td.setAttribute(atkey,atval);
                        }
                    });

                    $(tr).append(td);
                }
            });
            $('#tbBody').append(tr);

        })
    }

    function trIntoEdit($tr){
        $tr.find('td[edit-enable="true"]').each(function(){
            // $(this) 每一个td
            var editType = $(this).attr('edit-type');
            if(editType == 'select'){
                // 生成下拉框:找到数据源
                var deviceTypeChoices = GLOBAL_DICT[$(this).attr('global_key')];

                // 生成select标签
                var selectTag = document.createElement('select');
                var origin = $(this).attr('origin');

                $.each(deviceTypeChoices,function(k,v){
                    var option = document.createElement('option');
                    $(option).text(v[1]);
                    $(option).val(v[0]);
                    if(v[0] == origin){
                        // 默认选中原来的值
                        $(option).prop('selected',true);
                    }
                    $(selectTag).append(option);
                });

                $(this).html(selectTag);
                // 显示默认值
            }else{
                // 获取原来td中的文本内容
                var v1 = $(this).text();
                // 创建input标签，并且内部设置值
                var inp = document.createElement('input');
                $(inp).val(v1);
                // 添加到td中
                $(this).html(inp);
            }


        });
    }
    function trOutEdit($tr){
        $tr.find('td[edit-enable="true"]').each(function(){
            // $(this) 每一个td
            var editType = $(this).attr('edit-type');
            if(editType == 'select'){
                var option = $(this).find('select')[0].selectedOptions;
                $(this).attr('new-origin',$(option).val());
                $(this).html($(option).text());
            }else{
                var inputVal = $(this).find('input').val();
                $(this).html(inputVal);
            }

        });
    }
    jq.extend({
        // xx: function (url) {
        xx: function (url) {
            initial(url);

            // 所有checkbox绑定事件
            $('#tbBody').on('click',':checkbox',function(){
                // $(this) // checkbox标签
                // 1. 检测是否已经被选中
                if($('#inOutEditMode').hasClass('btn-warning')){
                    var $tr = $(this).parent().parent();
                    if($(this).prop('checked')){
                        // 进入编辑模式
                        trIntoEdit($tr);
                    }else{
                        // 退出编辑模式
                        trOutEdit($tr);
                    }
                }
            });

            // 所有按钮绑定事件
            $('#checkAll').click(function(){
                if($('#inOutEditMode').hasClass('btn-warning')){
                    $('#tbBody').find(':checkbox').each(function(){
                        if(!$(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trIntoEdit($tr);
                            $(this).prop('checked',true);
                        }
                    })
                }else{
                    $('#tbBody').find(':checkbox').prop('checked',true);
                }

            });

            $('#checkReverse').click(function(){
                if($('#inOutEditMode').hasClass('btn-warning')){
                    $('#tbBody').find(':checkbox').each(function(){
                        var $tr = $(this).parent().parent();
                        if($(this).prop('checked')){
                            trOutEdit($tr);
                            $(this).prop('checked',false);
                        }else{
                            trIntoEdit($tr);
                            $(this).prop('checked',true);
                        }
                    })
                }else{
                    $('#tbBody').find(':checkbox').each(function(){
                        var $tr = $(this).parent().parent();
                        if($(this).prop('checked')){
                            $(this).prop('checked',false);
                        }else{
                            $(this).prop('checked',true);
                        }
                    })
                }
            });

            $('#checkCancel').click(function(){
                if($('#inOutEditMode').hasClass('btn-warning')){
                    $('#tbBody').find(':checkbox').each(function(){
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                            $(this).prop('checked',false);
                        }
                    })
                }else{
                    $('#tbBody').find(':checkbox').prop('checked',false);
                }
            });

            $('#inOutEditMode').click(function(){
                if($(this).hasClass('btn-warning')){
                    // 退出编辑模式
                    $(this).removeClass('btn-warning');
                    $(this).text('进入编辑模式');
                    $('#tbBody').find(':checkbox').each(function(){
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                        }
                    })
                }else{
                    // 进入编辑模式
                    $(this).addClass('btn-warning');
                    $(this).text('退出编辑模式');

                    $('#tbBody').find(':checkbox').each(function(){
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trIntoEdit($tr);
                        }
                    })
                }
            });

            $('#multiDel').click(function(){
                // $('#tbBody').find(':checkbox')
                var idList = [];
                $('#tbBody').find(':checked').each(function(){
                    var v = $(this).val();
                    idList.push(v)
                });

                $.ajax({
                    url: url,
                    type: 'delete',
                    data: JSON.stringify(idList),
                    success:function(arg){
                        console.log(arg);
                    }
                })

            });

            $('#refresh').click(function(){
                initial(url)
            });

            $('#save').click(function(){
                if($('#inOutEditMode').hasClass('btn-warning')){

                     $('#tbBody').find(':checkbox').each(function(){
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                        }
                    })

                }

                var all_list = [];
                // 获取用户修改过的数据
                $('#tbBody').children().each(function(){
                    // $(this) = tr
                    var $tr= $(this);
                    var nid= $tr.attr('nid');
                    var row_dict = {};
                    var flag = false;
                    $tr.children().each(function(){
                        if($(this).attr('edit-enable')) {
                            if($(this).attr('edit-type') == 'select'){
                                var newData = $(this).attr('new-origin');
                                var oldData = $(this).attr('origin');
                                if(newData){
                                    if (newData != oldData) {
                                        var name = $(this).attr('name');
                                        row_dict[name] = newData;
                                        flag = true;
                                    }
                                }

                            }else{
                                var newData = $(this).text();
                                var oldData = $(this).attr('origin');
                                if (newData != oldData) {
                                    var name = $(this).attr('name');
                                    row_dict[name] = newData;
                                    flag = true;
                                }
                            }

                        }

                    });
                    if(flag){
                        row_dict['id'] = nid;
                    }
                    all_list.push(row_dict)

                });

                // 通过Ajax提交后台
                $.ajax({
                    url: url,
                    type: 'PUT',
                    data: JSON.stringify(all_list),
                    success:function(arg){
                        console.log(arg);
                    }
                })
            });

            $('.search-list').on('click','li',function(){
                // 点击li执行函数
                var wenben = $(this).text();
                var searchType = $(this).attr('search_type');
                var name = $(this).attr('name');
                var globalName = $(this).attr('global_name');

                // 把显示替换
                $(this).parent().prev().find('.searchDefault').text(wenben);


                if(searchType == 'select'){
                    /*
                        [
                            [1,‘文本’],
                            [1,‘文本’],
                            [1,‘文本’],
                        ]
                     */
                    var sel = document.createElement('select');
                    $(sel).attr('class','form-control');
                    $(sel).attr('name',name);
                    $.each(GLOBAL_DICT[globalName],function(k,v){
                        var op = document.createElement('option');
                        $(op).text(v[1]);
                        $(op).val(v[0]);
                        $(sel).append(op);
                    });
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(sel);
                }else{
                    var inp = document.createElement('input');
                    $(inp).attr('class','form-control');
                    $(inp).attr('name',name);
                      $(inp).attr('type','text');
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(inp);
                }

            });

            // 搜索+号键
            $('.search-list').on('click','.add-search-condition',function(){
                // 拷贝的新一搜索项
                var newSearchItem = $(this).parent().parent().clone();
                $(newSearchItem).find('.add-search-condition span').removeClass('glyphicon-plus').addClass('glyphicon-minus');
                $(newSearchItem).find('.add-search-condition').addClass('del-search-condition').removeClass('add-search-condition');
                $('.search-list').append(newSearchItem);

            });

             $('.search-list').on('click','.del-search-condition',function(){
                 $(this).parent().parent().remove();
             });

            $('#doSearch').click(function(){
                initial(url);
            })

            // $('.M-box3').pagination({
            //     // pageCount: 5,
            //     jump: true,
            //     coping: true,
            //     homePage: '首页',
            //     endPage: '末页',
            //     prevContent: '上页',
            //     nextContent: '下页',
            //     // showData : 10,
            //     callback: function (api) {
            //         console.log(api.getCurrent());
            //         api.setPageCount(5);
            //         initial(url,api.getCurrent())
            //     }
            // });


        }
    })
})(jQuery);