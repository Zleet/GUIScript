# ==============================================================================
# Short script to construct the two snippets of code required for creating
# a twenty button "set total loops" window
# ==============================================================================
def main():

    # build the code for the 20 buttons
    template_1 = '# "Set total loops to {{total_loops}}" button' + "\n"
    template_1 += "total_loops_button_{{total_loops}} = ttk.Button(set_total_loops_frame, text='{{total_loops}}', width=3," + "\n"
    template_1 += "\t\t\t\t\tcommand=set_total_loops_to_{{total_loops}})" + "\n"
    template_1 += "total_loops_button_{{total_loops}}.grid(row={{row}}, column={{col}}, sticky=W)" + "\n\n"

    python_code = ''

    for row in range(4):
        for col in range(5):
            total_loops = (row * 5) + col + 1
            print(total_loops)
            code_to_add = template_1
            code_to_add = code_to_add.replace('{{total_loops}}', str(total_loops))
            code_to_add = code_to_add.replace('{{row}}', str(row + 1))
            code_to_add = code_to_add.replace('{{col}}', str(col))
            python_code += code_to_add

    # write code to outfie
    outfile = open('twenty_button_code.py', 'w')
    outfile.write(python_code)
    outfile.close()

    # build the code for the twenty separate handler functions
    template_2 = "# ==============================================================================\n"
    template_2 += "# Set the total loops in the total_loops_text_box to {{total_loops}}\n"
    template_2 += "# ==============================================================================\n"
    template_2 += "def set_total_loops_to_{{total_loops}}():\n"
    template_2 += "\n"
    template_2 += "# clear out the text in the total loops text box\n"
    template_2 += "total_loops_text_box.delete(1.0, END)\n"
    template_2 += "\n"
    template_2 += "# set the text in the total loops text box to total_loops\n"
    template_2 += 'total_loops_text_box.insert(END, "{{total_loops}}")' + "\n"
    template_2 += "\n"
    template_2 += "return\n"

    python_code_2 = ''

    for total_loops in range(1, 21):
        code_to_add = template_2
        code_to_add = code_to_add.replace('{{total_loops}}', str(total_loops))
        python_code_2 += code_to_add

    # write code to outfile
    outfile = open('twenty_function_code.py', 'w')
    outfile.write(python_code_2)
    outfile.close()

    return
# ===============================================================================
main()
