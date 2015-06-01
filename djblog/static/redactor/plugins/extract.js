if (!RedactorPlugins) var RedactorPlugins = {};
 
RedactorPlugins.more = function()
{
    return {
        init: function()
        {
            var button = this.button.add('more', 'More');
 
            // make your added button as Font Awesome's icon
            this.button.setAwesome('more', 'fa-ellipsis-h');
 
            this.button.addCallback(button, this.more.doMore);
        },
        doMore: function(buttonName)
        {
            alert(buttonName);
        }
    };
};
