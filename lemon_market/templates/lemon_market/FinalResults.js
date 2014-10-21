$(function () {
    $('#container').highcharts({
        title: {
            text: 'Results',
        },
        xAxis: {
            categories: ['Round 1', 'Round 2', 'Round 3'],
        },
        yAxis: {
            title: {
                text: 'Points'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: 'points'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [
        {
            name: 'Transaction Price',
            data: [
            {% for round in rounds %}
            {% if forloop.counter0 %},{% endif %}
            {{round.seller.price|default:"null"}}
            {% endfor %}
                ],
        }
        {% for player in group.get_players %}
        ,{
            name: 'Earnings for {{player.role|capfirst}}',
            data: [
            {% for round in player.me_in_all_rounds %}
            {% if forloop.counter0 %}
            ,
                {% endif %}
            {{round.earnings|floatformat}}
                {% endfor %}
            ]
        }
            {% endfor %}
            ]
    });
});
