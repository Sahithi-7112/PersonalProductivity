import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class PassValid extends JFrame {
    private JPasswordField passField;
    private JLabel resLbl;

    public PassValid() {
        setTitle("Pass Validator");
        setSize(350, 200);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new FlowLayout());

        JLabel lbl = new JLabel("Enter Pass:");
        passField = new JPasswordField(15);
        JButton valBtn = new JButton("Validate");
        resLbl = new JLabel("Result will show here.");

        valBtn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                valPass();
            }
        });

        add(lbl);
        add(passField);
        add(valBtn);
        add(resLbl);
        
        setVisible(true);
    }

    private void valPass() {
        String pass = new String(passField.getPassword());

        if (pass.length() < 8) {
            resLbl.setText("Min 8 chars needed.");
        } else if (!pass.matches(".*[A-Z].*")) {
            resLbl.setText("Need an uppercase letter.");
        } else if (!pass.matches(".*\\d.*")) {
            resLbl.setText("Need a digit.");
        } else if (!pass.matches(".*[@#$%^&+=].*")) {
            resLbl.setText("Need a special char.");
        } else {
            resLbl.setText("Strong Pass! ✅");
        }
    }

    public static void main(String[] args) {
        new PassValid();
    }
}
