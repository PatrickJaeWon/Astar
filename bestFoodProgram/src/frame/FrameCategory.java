package frame;

import static frame.Constant.*;

import java.awt.Choice;
import java.awt.Color;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;

import restaurantDB.RestaurantList;

public class FrameCategory extends JPanel{
	
	public FrameCategory(RestaurantList restaurantList) {
		setBackground(new Color(255, 192, 203));
		setLayout(null);
		setSize(400, 700);
		
		Choice md = new Choice();
		   
	    JLabel choiceName = new JLabel("선호하는 취향:");
	                    
	    choiceName.setSize(150,100);
	    choiceName.setLocation(60,25);
	    choiceName.setBackground(Color.BLACK);
	    choiceName.setFont(new Font("여기어때 잘난체", Font.BOLD, 21));
	    add(choiceName);
	      
	      
	    md.add("선택안함");
	    md.add("조용한");
	    md.add("깔끔한");
	    md.add("가성비좋은");
	      
	    md.setSize(170,0);
	    md.setLocation(212,63);
	    md.setBackground(Color.pink);
	    md.setFont(new Font("여기어때 잘난체", Font.BOLD, 13));

	      
	    add(md);

		
		ImageIcon buttonImageKorean = new ImageIcon("./src/카테고리_한식.png");
		ImageIcon buttonImageChinese = new ImageIcon("./src/카테고리_중식.png");
		ImageIcon buttonImageJapanese = new ImageIcon("./src/카테고리_일식.png");
		ImageIcon buttonImageWestern = new ImageIcon("./src/카테고리_양식.png");
		ImageIcon buttonImageFastfood = new ImageIcon("./src/카테고리_패스트푸드.png");
		ImageIcon buttonImageSalad = new ImageIcon("./src/카테고리_샐러드.png");
		ImageIcon buttonImageAllfood = new ImageIcon("./src/카테고리_전체.png");
		
		JButton btnKorean = new JButton(buttonImageKorean);
		JButton btnChinese = new JButton(buttonImageChinese);
		JButton btnJapanese = new JButton(buttonImageJapanese);
		JButton btnWestern = new JButton(buttonImageWestern);
		JButton btnFastfood = new JButton(buttonImageFastfood);
		JButton btnSalad = new JButton(buttonImageSalad);
		JButton btnAllfood = new JButton(buttonImageAllfood);

		btnKorean.setSize(127, 100);
		btnKorean.setBorderPainted(false);
		btnKorean.setContentAreaFilled(false);
		btnKorean.setFocusPainted(false);
		
		btnKorean.setLocation(
				((int) getSize().getWidth() /2 -145), 
				(int) getLocation().getY() / 2 + 100);
				
		btnChinese.setSize(127, 100);
		btnChinese.setBorderPainted(false);
		btnChinese.setContentAreaFilled(false);
		btnChinese.setFocusPainted(false);
		
		btnChinese.setLocation(
				(int) btnKorean.getLocation().getX() + 155, 
				(int) btnKorean.getLocation().getY());
				
		btnJapanese.setSize(127, 100);
		btnJapanese.setBorderPainted(false);
		btnJapanese.setContentAreaFilled(false);
		btnJapanese.setFocusPainted(false);
		
		btnJapanese.setLocation(
				((int) btnKorean.getLocation().getX()), 
				(int) btnKorean.getLocation().getY() + 125);
				
		btnWestern.setSize(127, 100);
		btnWestern.setBorderPainted(false);
		btnWestern.setContentAreaFilled(false);
		btnWestern.setFocusPainted(false);
		
		btnWestern.setLocation(
				(int) btnJapanese.getLocation().getX() + 155, 
				(int) btnJapanese.getLocation().getY());
				
		btnFastfood.setSize(127, 100);
		btnFastfood.setBorderPainted(false);
		btnFastfood.setContentAreaFilled(false);
		btnFastfood.setFocusPainted(false);
		
		btnFastfood.setLocation(
				(int) btnKorean.getLocation().getX(), 
				(int) btnJapanese.getLocation().getY() + 125);
				
		btnSalad.setSize(127, 100);
		btnSalad.setBorderPainted(false);
		btnSalad.setContentAreaFilled(false);
		btnSalad.setFocusPainted(false);
		
		btnSalad.setLocation(
				(int) btnFastfood.getLocation().getX() + 155, 
				(int) btnFastfood.getLocation().getY());
		
		btnAllfood.setSize(285, 100);
		btnAllfood.setBorderPainted(false);
		btnAllfood.setContentAreaFilled(false);
		btnAllfood.setFocusPainted(false);
		
		btnAllfood.setLocation(
				(int) btnKorean.getLocation().getX(), 
				(int) btnFastfood.getLocation().getY() + 125);
		
		add(btnKorean);
		add(btnChinese);
		add(btnJapanese);
		add(btnWestern);
		add(btnFastfood);
		add(btnSalad);
		add(btnAllfood);
		
		//하단메뉴
		JButton btnEnd = new JButton("");
		JButton btnBack = new JButton("");
		JButton btnHome = new JButton("");
		
		btnEnd.setSize(50, 50);
		btnEnd.setBorderPainted(false);
		btnEnd.setContentAreaFilled(false);
		btnEnd.setFocusPainted(false);
		
		btnEnd.setLocation(
				((int) getSize().getWidth() /2 + 90),
				(int) getLocation().getY() / 2 + 630);
				
		btnBack.setSize(50, 50);
		btnBack.setBorderPainted(false);
		btnBack.setContentAreaFilled(false);
		btnBack.setFocusPainted(false);
		
		btnBack.setLocation(
				((int) getSize().getWidth() /2 -27), 
				(int) getLocation().getY() / 2 + 630);
				
		btnHome.setSize(50, 50);
		btnHome.setBorderPainted(false);
		btnHome.setContentAreaFilled(false);
		btnHome.setFocusPainted(false);
		
		btnHome.setLocation(
				((int) getSize().getWidth() /2 -138), 
				(int) getLocation().getY() / 2 + 630);
				
		add(btnEnd);
		add(btnBack);
		add(btnHome);
		
		btnKorean.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameCategoryChioce(restaurantList, KOREAN, md.getSelectedItem(), 0, 0));
				
			}
		});
		
		btnChinese.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameCategoryChioce(restaurantList, CHINESE, md.getSelectedItem(), 0, 0));
				
			}
		});
		
		btnJapanese.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameCategoryChioce(restaurantList, JAPANESE, md.getSelectedItem(), 0, 0));
				
			}
		});
		
		btnWestern.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameCategoryChioce(restaurantList, WESTERN, md.getSelectedItem(), 0, 0));
				
			}
		});
		
		btnFastfood.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameCategoryChioce(restaurantList, FASTFOOD, md.getSelectedItem(), 0, 0));
				
			}
		});
		
		btnSalad.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameCategoryChioce(restaurantList, SALAD, md.getSelectedItem(), 0, 0));
				
			}
		});
		
		btnAllfood.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameCategoryChioce(restaurantList, "ALL", md.getSelectedItem(), 0, 0));
				
			}
		});
		
		btnEnd.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
				
			}
		});
		
		btnBack.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameBegin());
				
			}
		});
		
		btnHome.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameFrist());
				
			}
		});
	}

}
