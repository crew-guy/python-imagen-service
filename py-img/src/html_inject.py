
def inject_context_in_html(template_name, data_obj):
    template_filename = ''
    context = {}
    if template_name == 'COMMUNITY':
        template_filename = env.get_template("combat.html")
    elif template_name == 'COMBAT':
        template_filename = env.get_template("combat.html")
        combat_data = data_obj
        combat_date = parser.parse(combat_data["starts_at"])
        combat_day = combat_date.strftime("%d %b %Y")
        combat_time = combat_date.strftime("%H:%M %p")
        quiz_details = combat_data["quiz_details"]
        topics = [topic["name"] for topic in combat_data["topic_groups"]]
        context ={
            'name':combat_data["name"], 
            'time':combat_time, 
            'date':combat_day,
            'topics':topics, 
            'details':[f'{quiz_details["section"]} round', f'{quiz_details["questions"]} questions'], 
            'duration':f'{quiz_details["duration"]} mins', 
            'coupon_code':'ANK2001' 
            }
    
    template = env.get_template(template_filename)
    
    print(context)
    return template.render(context=context)
