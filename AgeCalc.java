import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

import java.time.Year;

public class AgeCalc extends JFrame {
    private JTextField yearField;
    private JLabel resLabel;

    public AgeCalc() {
        setTitle("Age Calc");
        setSize(300, 200);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new FlowLayout());

        JLabel lbl = new JLabel("Birth Year:");
        yearField = new JTextField(10);
        JButton calcBtn = new JButton("Calc Age");
        resLabel = new JLabel("Age will show here.");

        calcBtn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                calcAge();
            }
        });

        add(lbl);
        add(yearField);
        add(calcBtn);
        add(resLabel);
        
        setVisible(true);
    }

    private void calcAge() {
        try {
            int birthYr = Integer.parseInt(yearField.getText());
            int currYr = Year.now().getValue();

            if (birthYr > currYr || birthYr < 1900) {
                JOptionPane.showMessageDialog(this, "Enter a valid year (1900 - Now).", 
                                              "Invalid!", JOptionPane.WARNING_MESSAGE);
                return;
            }

            int age = currYr - birthYr;
            resLabel.setText("Age: " + age + " yrs");
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(this, "Invalid! Enter a number.", 
                                          "Error!", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        new AgeCalc();
    }
}
