/* 
    Version     : 1.0
    Released on : 12.02.2021
    Author      : Sergey Kharchishin 
    Url         : https://izocolorpicker.rukovoditel.net/
    License     : MIT License

    Copyright (c) 2021
    Sergey Kharchishin (www.rukovoditel.net)
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE

 */

class izoColorPicker
{
    constructor(element, options)
    {
        //defautl options
        let defaults = {
            onApply: false,
            onSave: false,
            onRemove: false,
            buttonApplyTitle: 'Apply',
            buttonCancelTitle: 'Cancel',
            myColors: '',
        }

        this.options = $.extend({}, defaults, options)
        
        this.selectedCorlor = '';

        /**
         * Get element
         */
        this.element = $(element);
        this.isInput = this.element.is('input')
        
        if(this.isInput)
        {
            this.selectedCorlor = this.element.val();        
        }
        else
        {
            this.inputElement = this.element.find('input:first')
            this.buttonElement = this.element.find('button:first')
            
            let dataColor = this.element.attr('data-color') 
            if(typeof dataColor != 'undefined')
            {
                this.selectedCorlor = dataColor;
            }
            else if(this.inputElement.length>0)
            {
                this.selectedCorlor = this.inputElement.val()
            }                           
        }
        
        /**
         * Set default colors
         * using Map() oject to easy setup colors
         * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map
         */
        this.colors = new Map()
        this.setColors()
        
        /**
         * Prepare saved color list
         * Using Set() object where items are unique
         * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set
         */
        this.savedColors = new Set();
        this.setSavedColors()
                
        /**
         * Prepare html template
         */
        this.template = '<div class="izoColorPicker-popup">'+
                            '<div class="izoColorPicker-row">'+
                                '<div class="izoColorPicker-input-clearable">'+
                                    '<input type="text" class="izoColorPicker-input-color" maxlength="7">'+
                                    '<i class="izoColorPicker-icon-clear">&times;</i>'+
                                '</div>'+
                                '<input type="color" class="izoColorPicker-color-preview" value="#ffffff">'+ 
                                '<button type="button" class="izoColorPicker-save-color">+</button>'+
                                '<button type="button" class="izoColorPicker-remove-color" style="display:none">&times;</button>'+
                            '</div>'+
                            '<div class="izoColorPicker-saved-colors-row"></div>'+
                            '<div class="izoColorPicker-row">'+this.render9colors()+'</div>'+
                            '<div class="izoColorPicker-row izoColorPicker-row-8colors"></div>'+
                            '<div class="izoColorPicker-buttons">'+
                                '<button class="izoColorPicker-button izoColorPicker-button-apply" type="button">'+this.options.buttonApplyTitle+'</button>'+
                                '<button class="izoColorPicker-button izoColorPicker-button-cancel" type="button">'+this.options.buttonCancelTitle+'</button>'+
                            '</div>'+    
                        '</div>'

        //build picker object                
        this.picker = $(this.template)

        /*
         * Prepare events
         * click - this is the main even where we check where customer click in Color Picker popup and do some actions
         * resize - check if window resized and chagne popup position if it needs
         * mousedown - if user click outside of Color Picker puopup then close popup
         */
        this._events = [
            [this.picker, {
                    click: $.proxy(this.click, this)
                }],               
            [$(window), {
                    resize: $.proxy(this.place, this)
                }],
            [$(document), {
                    mousedown: $.proxy(function (e) {
                        // Clicked outside the datepicker, hide it
                        if (!(
                                this.element.is(e.target) ||
                                this.element.find(e.target).length ||
                                this.picker.is(e.target) ||
                                this.picker.find(e.target).length
                                )) {
                            
                            if(this.picker.hasClass('izoColorPicker-popup-lock'))
                            {
                                this.picker.removeClass('izoColorPicker-popup-lock') 
                            }
                            else
                            {
                                this.remove();
                            }
                        }
                    }, this)
                }]
        ];
    }
    setColors()
    {
        this.colors.set('#000000',['#000000','#212121','#424242','#616161','#757575','#9E9E9E','#BDBDBD','#FFFFFF'])
        this.colors.set('#F44336',['#D32F2F','#E53935','#F44336','#EF5350','#E57373','#EF9A9A','#FFCDD2','#FFEBEE'])
        this.colors.set('#FF9800',['#F57C00','#FB8C00','#FF9800','#FFA726','#FFB74D','#FFCC80','#FFE0B2','#FFF3E0'])
        this.colors.set('#FFEB3B',['#FBC02D','#FDD835','#FFEB3B','#FFEE58','#FFF176','#FFF59D','#FFF9C4','#FFFDE7'])
        this.colors.set('#8BC34A',['#689F38','#7CB342','#8BC34A','#9CCC65','#AED581','#C5E1A5','#DCEDC8','#F1F8E9'])
        this.colors.set('#009688',['#00796B','#00897B','#009688','#26A69A','#4DB6AC','#80CBC4','#B2DFDB','#E0F2F1'])
        this.colors.set('#03A9F4',['#0288D1','#039BE5','#03A9F4','#29B6F6','#4FC3F7','#81D4FA','#B3E5FC','#E1F5FE'])
        this.colors.set('#3F51B5',['#303F9F','#3949AB','#3F51B5','#5C6BC0','#7986CB','#9FA8DA','#C5CAE9','#E8EAF6'])
        this.colors.set('#9C27B0',['#7B1FA2','#8E24AA','#9C27B0','#AB47BC','#BA68C8','#CE93D8','#E1BEE7','#F3E5F5'])
    }
    render9colors()
    {      
        let html = '<div class="izoColorPicker-9colors">'
        
        this.colors.forEach((value,key)=>{
            html += '<div class="izoColorPicker-9c-item '+(value.includes(this.selectedCorlor) ? 'izoColorPicker-9c-item-current':'')+'" data-color="'+key+'" style="background-color:'+key+'"></div>'                        
        })
        html += '</div>';
        
        return html
    }
    render8colors(color)
    {
        if(!this.colors.has(color)) return false
        
        let html = '<div class="izoColorPicker-8colors">'
                
        this.colors.get(color).forEach((value,key)=>{
            html += '<div class="izoColorPicker-8c-item '+(((value==color && this.selectedCorlor.lenght==0) || value==this.selectedCorlor) ? 'izoColorPicker-8c-item-current':'')+'" data-color="'+value+'" style="background-color:'+value+'"></div>'
        })
        html += '</div>';
        
        $('.izoColorPicker-row-8colors',this.picker).html(html)
    }
    remove()
    {        
        this._unapplyEvents(this._events);
        this.picker.remove()   
        delete this.element.data().izoColorPicker;
    }
    _applyEvents(evs) {
        for (var i = 0, el, ev; i < evs.length; i++) {
            el = evs[i][0];
            ev = evs[i][1];
            el.on(ev);
        }
        
        $('.izoColorPicker-input-color',this.picker).on('input',$.proxy(this.setColorFromInput, this))
        
        
        /*
         *Detect if user click on input type="color" and selecting some color
         *https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/color#javascript
         */
        const that = this;
        let colorWell = document.querySelector(".izoColorPicker-color-preview");        
        colorWell.addEventListener("input", function(event){ 
            that.selectColor(event.target.value) 
            that.resectSelection()
        }, false);        
        colorWell.select();
    }
    _unapplyEvents(evs) {
        for (var i = 0, el, ev; i < evs.length; i++) {
            el = evs[i][0];
            ev = evs[i][1];
            el.off(ev);
        }
        
        $('.izoColorPicker-input-color',this.picker).off('input')
    }
    click(e)
    {
        /*
         * detect where customer clicked in popup and do actions 
         */
        
        let target = $(e.target).closest('div,button,i,input');
        if (target.length == 1)
        {                        
            let className = target[0].className.trim()
           
            switch (true)
            {
                //select defautl color
                case className.includes('izoColorPicker-9c-item'):
                    this.resectSelection()
                    $(target[0]).addClass('izoColorPicker-9c-item-current')
                    this.selectColor($(target[0]).attr('data-color'))
                    this.render8colors($(target[0]).attr('data-color'))
                    break;
                
                //select color from 8 choices
                case className.includes('izoColorPicker-8c-item'):                    
                    this.resectSelection(false)
                    $(target[0]).addClass('izoColorPicker-8c-item-current')
                    this.selectColor($(target[0]).attr('data-color'))
                    break;
                 
                //select saved color
                case className.includes('izoColorPicker-sc-item'):                    
                    this.resectSelection()
                    $(target[0]).addClass('izoColorPicker-sc-item-current')
                    this.selectColor($(target[0]).attr('data-color'))
                    this.showRemoveButton()
                    break;    
                    
                //cancle and close popup    
                case className.includes('izoColorPicker-button-cancel'):
                    this.remove()
                    break;
                
                //apply selected color
                case className.includes('izoColorPicker-button-apply'):
                    if(this.isInput)
                    {
                        this.element.val(this.selectedCorlor)
                    }
                    else
                    {
                        this.element.attr('data-color',this.selectedCorlor)
                        
                        if(this.inputElement.length>0)
                        {
                            this.inputElement.val(this.selectedCorlor)
                        }
                        
                        if(this.buttonElement.length>0)
                        {
                            this.buttonElement.css('background-color',this.selectedCorlor)
                        }
                        
                        if((this.inputElement.length==0 || this.inputElement.attr('type')=='hidden') && this.buttonElement.length==0)
                        {
                            this.element.css('background-color',this.selectedCorlor)
                        }
                    }
                    
                    /*
                     * Call onApply function if setup
                     * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/call
                     */
                    if(this.options.onApply) this.options.onApply.call(this,this.selectedCorlor);
                    
                    this.remove()
                    break;    
                
                //reset input field
                case className.includes('izoColorPicker-icon-clear'):                    
                    this.resectSelection()
                    this.selectColor('')                    
                    break; 
                
                //click on preview
                case className.includes('izoColorPicker-color-preview'): 
                    this.picker.addClass('izoColorPicker-popup-lock')
                    break;
                
                //save color
                case className.includes('izoColorPicker-save-color'): 
                    this.resectSelection()
                    this.saveColor()                                       
                    break;
                
                //remove color
                case className.includes('izoColorPicker-remove-color'): 
                    this.resectSelection()
                    this.hideRemoveButton()
                    this.removeColor()
                    break;    
                    
                                                    
            }
        }
    }
    showRemoveButton()
    {
        $('.izoColorPicker-remove-color', this.picker).show()
        $('.izoColorPicker-save-color', this.picker).hide()
        
    }
    hideRemoveButton()
    {
        $('.izoColorPicker-remove-color', this.picker).hide()
        $('.izoColorPicker-save-color', this.picker).show()
        
    }
    removeColor()
    {
        this.savedColors.delete(this.selectedCorlor)        
        this.setCookie('izoColorPickerColors',Array.from(this.savedColors))                                
        this.renderSavedColors()
        
        if(this.options.onRemove) this.options.onRemove.call(this,this.selectedCorlor,Array.from(this.savedColors));
        
        this.resectSelection()
        this.selectColor('')  
    }
    resectSelection(reset9c = true)
    {
        if(reset9c) $('.izoColorPicker-9c-item', this.picker).removeClass('izoColorPicker-9c-item-current')
        
        $('.izoColorPicker-8c-item', this.picker).removeClass('izoColorPicker-8c-item-current')
        $('.izoColorPicker-sc-item', this.picker).removeClass('izoColorPicker-sc-item-current')
        this.hideRemoveButton()
    }
    saveColor()
    {
        if(this.selectedCorlor.length!=7) return false
               
        this.savedColors.add(this.selectedCorlor)
        
        this.setCookie('izoColorPickerColors',Array.from(this.savedColors))
                                
        this.renderSavedColors()
        
        if(this.options.onSave) this.options.onSave.call(this,this.selectedCorlor,Array.from(this.savedColors));
    }
    renderSavedColors()
    {
        if(this.savedColors.size==0)
        {
            $('.izoColorPicker-saved-colors-row',this.picker).html('')
            return false
        }
                        
        let html= '<div class="izoColorPicker-row">'
        this.savedColors.forEach((value)=>{
            html += '<div class="izoColorPicker-sc-item '+(value == this.selectedCorlor ? 'izoColorPicker-sc-item-current':'')+'" data-color="'+value+'" style="background-color:'+value+'"></div>'                        
        })
        
        html += '</div>'
        
        $('.izoColorPicker-saved-colors-row',this.picker).html(html)
    }
    setSavedColors()
    {                
        let colors = this.getCookie('izoColorPickerColors')
         
        if(this.options.myColors.length>0)
        {
            this.options.myColors.split(',').forEach(value=>this.savedColors.add(value))
        }
        
        if(colors.length>0)
        {                    
           colors.split(',').forEach((value)=>{
              this.savedColors.add(value) 
           }) 
        }                
    }
    selectColor(color)
    {
        if(color.length==0)
        {
            this.selectedCorlor = '';
            $('.izoColorPicker-input-color',this.picker).val('')
            $('.izoColorPicker-color-preview',this.picker).val('#ffffff')
        }
        else
        {        
            this.selectedCorlor = color

            $('.izoColorPicker-input-color',this.picker).val(color)
            $('.izoColorPicker-color-preview',this.picker).val(color)
        }
    }
    setColorFromInput()
    {
       this.selectedCorlor = $('.izoColorPicker-input-color',this.picker).val();
       
       if(this.selectedCorlor[0]!='#')
       {
           this.selectedCorlor = '#'+this.selectedCorlor
            $('.izoColorPicker-input-color',this.picker).val(this.selectedCorlor);  
       }
       
       if(this.selectedCorlor.length>0)
       {
            $('.izoColorPicker-color-preview',this.picker).val(this.selectedCorlor)
       }
       else
       {
           $('.izoColorPicker-color-preview',this.picker).val('#fff')
       }
    }
    show()
    {
        
        //append popup
        this.picker.appendTo('body');
                
        if(this.selectedCorlor.length>0)
        {
            this.selectColor(this.selectedCorlor)
            
            this.colors.forEach((value,key)=>{
               if(value.includes(this.selectedCorlor))
               {
                   this.render8colors(key)
               }
            })
        }
        else
        {
            this.render8colors('#000000')
        }
        
        this.renderSavedColors()
        
        this.place()
                
        this._unapplyEvents(this._events);
        this._applyEvents(this._events);
    }
    place()
    {
        let pickerWidth = this.picker.outerWidth(),
                pickerHeight = this.picker.outerHeight(),
                visualPadding = 10,
                windowWidth = $(window).width(),
                windowHeight = $(window).height(),
                scrollTop = $(window).scrollTop();

        //prepare z-index        
        let zIndex = parseInt(this.element.parents().filter(function () {
            return $(this).css('z-index') != 'auto';
        }).first().css('z-index')) + 10;
                
        var offset = this.element.offset();
        var height = this.element.outerHeight(false);
        var width = this.element.outerWidth(false);
        var left = offset.left,
                top = offset.top;

        //get left position        
        if (offset.left < 0)
        {
            left -= offset.left - visualPadding;
        }
        else if (offset.left + pickerWidth > windowWidth)
        {
            left = windowWidth - pickerWidth - visualPadding;
            
            this.picker.addClass('izoColorPicker-popup-right');
        }

        var yorient = 'bottom',
                top_overflow, bottom_overflow;
        
        //detect top postion
        top_overflow = -scrollTop + offset.top - pickerHeight;
        bottom_overflow = scrollTop + windowHeight - (offset.top + height + pickerHeight);
        if (Math.max(top_overflow, bottom_overflow) === bottom_overflow || bottom_overflow>pickerHeight)
        {
            yorient = 'top';
        }
        else
        {
            yorient = 'bottom';
        }
                
        this.picker.addClass('izoColorPicker-popup-' + yorient);
        
        if (yorient === 'top')
        {
            top += height + 5;
        }
        else
        {
            top -= pickerHeight + 5;
        }

        this.picker.css({
            top: top,
            left: left,
            zIndex: zIndex
        });
    }
    setCookie(name, value, options = {}) 
    {

        options = {
            path: '/',
            'max-age': (3600*24)*360,
            SameSite: 'Lax',
            ...options
        };

        if (options.expires instanceof Date) {
            options.expires = options.expires.toUTCString();
        }
        
        if(Array.isArray(value))
        {
            value = value.join(',')            
        }
        
        let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

        for (let optionKey in options) {
            updatedCookie += "; " + optionKey;
            let optionValue = options[optionKey];
            if (optionValue !== true) {
                updatedCookie += "=" + optionValue;
            }
        }

        document.cookie = updatedCookie;
    }
    getCookie(name) {
        let matches = document.cookie.match(new RegExp(
                "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
                ));
        return matches ? decodeURIComponent(matches[1]) : '';
    }
    static prepareDataColor(obj)
    {
        let element = $(obj)
        let isInput = element.is('input')
        
        if(!isInput)
        {
            let inputElement = element.find('input:first')
            let buttonElement = element.find('button:first')
            
            let dataColor = element.attr('data-color') 
            if(typeof dataColor != 'undefined')
            {
                if(buttonElement.length>0) buttonElement.css('background-color',dataColor)
                
                if(inputElement.length==0 || inputElement.attr('type')=='hidden')
                {
                   element.css('background-color',dataColor) 
                }                
            }                                                                                      
        }
    }
}

/*
 * Creating jQuery prototype
 * https://api.jquery.com/Types/#Prototype
 */

$(function () {
    $.fn.izoColorPicker = function (options)
    {
        this.each(function () {
            
            izoColorPicker.prepareDataColor(this)
            
            $(this).click(function () { 
                if(!$(this).data('izoColorPicker'))
                {
                    $(this).data('izoColorPicker',true)
                    
                    picker = new izoColorPicker(this, options)
                    picker.show()                    
                }
            })
        })
    }
})


