package frame;

import java.awt.Choice;
import java.awt.Color;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.SimpleDateFormat;
import java.util.Date;
import static frame.Constant.PLACE_NAME_BASIC;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

import restaurantDB.RestaurantList;

public class ReservationRandom extends JPanel{

	
	public ReservationRandom(RestaurantList restaurantList, String categoryName, String mood, int i) {
		//백그라운드 설정
		setBackground(new Color(255, 192, 203));
		setLayout(null);
		setSize(400, 700);
		
		//(전 페이지)음식 이미지 추출
		JLabel fImage=new JLabel(HtmlUtils.imgHtmlParser(restaurantList.Info().get(i).getImageUrl()));
        fImage.setSize(364,280);
        fImage.setLocation(18,70);
        add(fImage);
        
        
        JLabel choiceName = new JLabel(PLACE_NAME_BASIC+restaurantList.Info().get(i).getPlaceName());
        
	    choiceName.setSize(400,20);
	    choiceName.setLocation(40,370);
	    choiceName.setBackground(Color.BLACK);
	    choiceName.setFont(new Font("여기어때 잘난체", Font.BOLD, 21));
	    add(choiceName);
        
        
        
        
        //현재시간을 밀리
        long time = System.currentTimeMillis();
        
       SimpleDateFormat dayTime=new SimpleDateFormat("MM월 dd일(EE)");
       String str=dayTime.format(new Date(time)); 
       
        Choice reserTime=new Choice();
        String[] timeSlot= {
        		"시간대 선택",
        		str+"09:00AM",
        		str+"10:00AM",
        		str+"11:00AM",
        		str+"12:00PM",
        		str+"13:00PM",
        		str+"14:00PM",
        		str+"15:00PM",
        		str+"16:00PM",
        		str+"17:00PM",
        		str+"18:00PM",
        		str+"19:00PM",
        		str+"20:00PM"	
        		
        };//스트링 배열(에약시간)
        
        for (int j = 0; j < timeSlot.length; j++) {
        	reserTime.add(timeSlot[j]);
		}
        
        
        Choice NOpeople=new Choice();
        String[] NOpeopleList= {
        		"인원수 선택",
        		"1명",
        		"2명",
        		"3명",
        		"4명",
        		"5명",
        		"6명",
        		
        			
        		
        };//스트링 배열(인원수)
        
        for (int j = 0; j < NOpeopleList.length; j++) {
        	NOpeople.add(NOpeopleList[j]);
        	
		}
        
        
        NOpeople.setFont(new Font("나눔고딕코딩",Font.BOLD,16));
        NOpeople.setSize(340,190);
        NOpeople.setLocation(43,450);
        add(NOpeople);
        
        
        reserTime.setFont(new Font("나눔고딕코딩",Font.BOLD,16));
        reserTime.setSize(340,190);
        reserTime.setLocation(43,400);
        add(reserTime);
        
        
      //하단메뉴
      		JButton btnEnd = new JButton("");
      		JButton btnBack = new JButton("");
      		JButton btnHome = new JButton("");
      		
    		//에약버튼 생성
    		ImageIcon imageReservation = new ImageIcon("./src/예약완료.png");
    		JButton reserButton =new JButton(imageReservation);
    		//예약버튼 편집
    		reserButton.setSize(220,90);
    		reserButton.setBorderPainted(false);
    		reserButton.setContentAreaFilled(false);
    		reserButton.setFocusPainted(false);
    		reserButton.setLocation(90,515);
    		add(reserButton);
      		

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
      		add(reserButton);
      		
      		//버튼액션
      		
      		reserButton.addActionListener(new ActionListener() {
      			
      			@Override
      			public void actionPerformed(ActionEvent e) {
      				if(reserTime.getSelectedItem().equals("시간대 선택")) 
      					JOptionPane.showMessageDialog(null,"시간대를 선택해 주세요");
      				else {
      					if(NOpeople.getSelectedItem().equals("인원수 선택")) {
      						JOptionPane.showMessageDialog(null,"인원수를 선택해 주세요");
      					}
      					else {
      						JOptionPane.showMessageDialog(null,reserTime.getSelectedItem() + "\n" + NOpeople.getSelectedItem() + "\n" + "예약되었습니다.");
      						FrameBase.getDispose();
      						FrameBase.getInstance(new FrameBegin());
      					}
      					
      				}
      					
   
      				
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
    				FrameBase.getInstance(new FrameRandomChioce(restaurantList, categoryName,  mood, i));

    				
    			}
    		});
    		
    		btnHome.addActionListener(new ActionListener() {
    			
    			@Override
    			public void actionPerformed(ActionEvent e) {
    				FrameBase.getDispose();
    				FrameBase.getInstance(new FrameFrist());
    				
    			}
    		});
    		
        
	}//reservation
	
	

}