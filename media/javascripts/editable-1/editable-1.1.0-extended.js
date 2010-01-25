$(function(){
/*
 * Editable 1.1.0
 *
 * Copyright (c) 2009 Arash Karimzadeh (arashkarimzadeh.com)
 * Licensed under the MIT (MIT-LICENSE.txt)
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Date: Jan 13 2009
 */
$.fn.editable = function(options){
  var defaults = {
    onEdit: null,
    onSubmit: null,
    editClass: null,
    submit: null,
    cancel: null,
    type: 'text', //text, textarea or select
    submitBy: 'blur', //blur,change,dblclick,click
    options: null
  }
  var options = $.extend(defaults, options);
  
  var toEditable = function($this,options){
    $this.data('editable.current',$this.html());    
    $.editableFactory[options.type].toEditable($this.empty(),options);
    // Configure events,styles for changed content
    $this.unbind()
       .data('editable.previous',$this.data('editable.current'))
       .children()
         .focus()
         .addClass(options.editClass);
    // Submit Event
    if(options.submit){
      $('<button/>').appendTo($this)
            .html(options.submit)
            .unbind()   
            .mouseup(function(){toNonEditable($this,options,true)});
    }else
      $this.one(options.submitBy,function(){toNonEditable($this,options,true)})
         .children()
          .one(options.submitBy,function(){toNonEditable($this,options,true)});
    // Cancel Event
    if(options.cancel)
      $('<button/>').appendTo($this)
            .html(options.cancel)
            .unbind()
            .mouseup(function(){toNonEditable($this,options,false)});
    // Call User Function
    if($.isFunction(options.onEdit))
      options.onEdit.apply( $this,
                  [{
                    current:$this.data('editable.current'),
                    previous:$this.data('editable.previous')
                  }]
                );
  }
  var toNonEditable = function($this,options,change){
    // Configure events,styles for changed content
    $this.unbind()
       .click(function(){toEditable($this,options)})
       .data( 'editable.current',
            change 
            ?$.editableFactory[options.type].getValue($this,options)
            :$this.data('editable.current')
          )
       .html(
            options.type=='password'
              ?'*****'
            :$this.data('editable.current')
          );
    // Call User Function
    if($.isFunction(options.onSubmit))
      options.onSubmit.apply( $this,
                    [{
                      current: $this.data('editable.current'),
                      previous:$this.data('editable.previous')
                    }]
                  );
  }
    
  return  this.click(function(){toEditable($(this),options)});
}
$.editableFactory = {
  'text': {
    toEditable: function($this,options){
      $this.append('<input value="'+$this.data('editable.current')+'"/>');
    },
    getValue: function($this,options){
      return $this.children().val();
    }
  },
  'password': {
    toEditable: function($this,options){
      $this.append('<input type="password" value="'+$this.data('editable.current')+'"/>');
    },
    getValue: function($this,options){
      return $this.children().val();
    }
  },
  'textarea': {
    toEditable: function($this,options){
      $('<textarea/>').appendTo($this)
              .val($this.data('editable.current'));
    },
    getValue: function($this,options){
      return $this.children().val();
    }
  },
  'checkbox': {
    toEditable: function($this,options){
      $.each( options.options,
          function(){
            $('<input type="checkbox"/>').appendTo($this)
                  .val(this)
                  .after('<span>'+this+'</span>');
          }
        )
      var currentValues = $this.data('editable.current').split(',');
      $this.children(':checkbox').each(
        function(){
          if(currentValues.indexOf($(this).val())>-1)
            $(this).attr('checked', 'checked');
        }
      )
    },
    getValue: function($this,options){
      var items = [];
      $(':checkbox', $this).each(
        function(){
          if($(this).attr('checked'))
            items.push($(this).val());
        }
      )
      return items.join(',');
    }
  },
  'select': {
    toEditable: function($this,options){
      $select = $('<select/>').appendTo($this);
      $.each( options.options,
          function(key,value){
            $('<option/>').appendTo($select)
                  .html(value)
                  .attr('value',key);
          }
           )
      $select.children().each(
        function(){
          var opt = $(this);
          if(opt.text()==$this.data('editable.current'))
            return opt.attr('selected', 'selected').text();
        }
      )
    },
    getValue: function($this,options){
      var item = null;
      $('select', $this).children().each(
        function(){
          if($(this).attr('selected'))
            return item = $(this).text();
        }
      )
      return item;
    }
  }
}
});