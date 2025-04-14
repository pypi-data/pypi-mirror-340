def format_amount(amount):
    """
    格式化金额（保留2位小数）
    
    Args:
        amount (float|str): 金额
        
    Returns:
        str: 格式化后的金额字符串
    """
    return '{:.2f}'.format(float(amount))


def calculate_tax(amount, tax_rate, is_include_tax=False):
    """
    计算税额
    
    Args:
        amount (float|str): 金额
        tax_rate (float|str): 税率
        is_include_tax (bool): 是否含税，默认为False
        
    Returns:
        str: 税额（保留2位小数）
    """
    amount = float(amount)
    tax_rate = float(tax_rate)
    
    if is_include_tax:
        # 含税计算：税额 = 金额 / (1 + 税率) * 税率
        tax = amount / (1 + tax_rate) * tax_rate
    else:
        # 不含税计算：税额 = 金额 * 税率
        tax = amount * tax_rate
    
    return format_amount(tax)


def calculate_amount_without_tax(amount, tax_rate):
    """
    计算不含税金额
    
    Args:
        amount (float|str): 含税金额
        tax_rate (float|str): 税率
        
    Returns:
        str: 不含税金额（保留2位小数）
    """
    amount = float(amount)
    tax_rate = float(tax_rate)
    
    # 不含税金额 = 含税金额 / (1 + 税率)
    amount_without_tax = amount / (1 + tax_rate)
    
    return format_amount(amount_without_tax)


def calculate_amount_with_tax(amount, tax_rate):
    """
    计算含税金额
    
    Args:
        amount (float|str): 不含税金额
        tax_rate (float|str): 税率
        
    Returns:
        str: 含税金额（保留2位小数）
    """
    amount = float(amount)
    tax_rate = float(tax_rate)
    
    # 含税金额 = 不含税金额 * (1 + 税率)
    amount_with_tax = amount * (1 + tax_rate)
    
    return format_amount(amount_with_tax)


def amount_to_chinese(amount):
    """
    将金额转换为中文大写
    
    Args:
        amount (float|str): 金额
        
    Returns:
        str: 中文大写金额
    """
    amount = float(amount)
    
    if amount == 0:
        return '零元整'
    
    chn_num_char = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    chn_unit_char = ['', '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿', '拾', '佰', '仟', '万', '拾', '佰', '仟']
    chn_unit_section = ['', '万', '亿', '万亿']
    
    integer_part = int(amount)
    decimal_part = round((amount - integer_part) * 100)
    
    chinese_str = ''
    
    # 处理整数部分
    if integer_part > 0:
        integer_str = str(integer_part)
        integer_len = len(integer_str)
        
        section = 0
        section_pos = 0
        zero = True
        
        for i in range(integer_len - 1, -1, -1):
            digit = int(integer_str[integer_len - i - 1])
            
            if digit == 0:
                zero = True
            else:
                if zero:
                    chinese_str += chn_num_char[0]
                zero = False
                chinese_str += chn_num_char[digit] + chn_unit_char[i % 16]
            
            section_pos += 1
            if section_pos == 4:
                section += 1
                section_pos = 0
                zero = True
                chinese_str += chn_unit_section[section]
        
        chinese_str += '元'
    
    # 处理小数部分
    if decimal_part > 0:
        jiao = decimal_part // 10
        fen = decimal_part % 10
        
        if jiao > 0:
            chinese_str += chn_num_char[jiao] + '角'
        
        if fen > 0:
            chinese_str += chn_num_char[fen] + '分'
    else:
        chinese_str += '整'
    
    return chinese_str