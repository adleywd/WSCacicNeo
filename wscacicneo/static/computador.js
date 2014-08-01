var table = Ext.create('Ext.form.Panel', {
    renderTo: Ext.getBody(),
    title: '',
    height: 130,
    width: 280,
    style: {
            "text-align": 'left',
    },

    bodyPadding: 10,
    defaultType: 'textfield',
    items: [
        {
            fieldLabel: 'Nº Patrimônio',
            width:300,
            name: 'nome'
        },
        {
            xtype:'combobox',
            fieldLabel: 'Tipo',
            width: 300,
            name: 'tipo'
        },
        {
            fieldLabel: 'Marca',
            width:300,
            name: 'marca'
        },
        {
            xtype: 'button',
            text: 'Enviar',
            style:{
                margin: '0px 10px 0px 270px',
            }
        },
        {
            xtype: 'button',
            text: 'Limpar',
            style:{
                margin: '0px 10px 0px 0px',
            }
        },
    ]
});

painel = Ext.create('Ext.panel.Panel', {
        layout: 'fit',
        title: 'Computador',
        width: 425,
        height: 150,
        frame: true,
        draggable: true,
        collapsible: true,
        border : true,
        style: {
                "text-align": 'center',
                margin: '0px auto 15px auto'
        },
        items: table,
});

Ext.onReady(function(){


        Ext.create('Ext.Container', {
               padding: '15px',
               items: [painel],
        renderTo: 'widgets'
        });

});

