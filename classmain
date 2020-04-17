import ij.ImagePlus;
import ij.gui.*;
import ij.ImagePlus.*;
import ij.plugin.*;
import ij.process.ImageProcessor;
import ij.process.*;
import ij.gui.*;
import java.util.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import javax.imageio.ImageIO;
import javax.swing.JFrame;
import java.lang.Iterable;

public class ClassMain {
	
	public static void main (String[] args) {
		
/*OUVERTURE DE LA PILE TIFF (7 IMAGES DE DIMENSION 800X800) TELLE QUE 
 * CHACUNE DES IMAGES CORRESPOND A UN METAL (COUPLE A UN ANTICORPS)
 * EST MIS EN VALEUR DONC UN COMPARTIMENT D'INTERET EST MIS EN VALEUR*/	
		
/*LISTE DES CANAUX : 
 * sum (SUM DE TOUS LES MARQUEURS CI-DESSOUS)
In113
Nd143
Sm149
Gd160
Dy162
Ir191 (COUPLE A UN BIOMARQUEUR NUCLEAIRE)*/		
		
	 ImagePlus imp = new ImagePlus("C:/Users/Yvonne/Desktop/data3/tiffs/20190919_FluidigmBrCa_SE_s0_p8_r5_a5_ac_ilastik.tiff");
	

/* SEPARER LA PILE EN IMAGES INDIVIDUELLES*/
	 ImagePlus[] channels = ChannelSplitter.split(imp); 
	 
	
/*CONVERTION DES IMAGES INDIVIDUELLES IMAGEPLUS EN IMAGEPROCESSOR POUR LES MANIPULER AVEC LES METHODES DE CETTE CLASSE
 * (NE VOIS PAS COMMENT FAIRE LA CONVERTION DANS UNE BOUCLE)*/
	 ImageProcessor ip0 = channels[0].getProcessor(); 
	 ImageProcessor ip1 = channels[1].getProcessor(); 
	 ImageProcessor ip2 = channels[2].getProcessor(); 
	 ImageProcessor ip3 = channels[3].getProcessor(); 
	 ImageProcessor ip4 = channels[4].getProcessor(); 
	 ImageProcessor ip5 = channels[5].getProcessor(); 
	 ImageProcessor ip6 = channels[6].getProcessor(); 
	
/*APPLICATION DU FILTRE SMOOTH SUR TOUTES LES SLICES DE LA STACK*/	 
	 ip0.smooth();
	 ip1.smooth();
	 ip2.smooth();
	 ip3.smooth();
	 ip4.smooth();
	 ip5.smooth();
	 ip6.smooth();
	
	 
/*MISE A L'ECHELLE x2 DES IMAGES POUR MIEUX IDENTIFIER LES PIXELS APPARTENANT A TEL OU TEL COMPARTIMENT 
 * D'INTERET (NOYAU, MEMBRANE, FOND)*/	 
	 int height = ip6.getHeight();
	 int width = ip6.getWidth();
			 
	 ImageProcessor ip0resized = ip0.resize((2*height),(2*width));
	 ImageProcessor ip1resized = ip1.resize((2*height),(2*width));
	 ImageProcessor ip2resized = ip2.resize((2*height),(2*width));
	 ImageProcessor ip3resized = ip3.resize((2*height),(2*width));
	 ImageProcessor ip4resized = ip4.resize((2*height),(2*width));
	 ImageProcessor ip5resized = ip5.resize((2*height),(2*width));
	 ImageProcessor ip6resized = ip6.resize((2*height),(2*width));
	
	/*TEST DE LA NOUVELLE TAILLE DES IMAGES*/ 
	int height1 = ip6resized.getHeight();
//	System.out.println(height1);
	
	/*TABLEAU DANS LE CAS D'UNE BOUCLE SUR TOUTES LES IMAGES DE LA PILE*/
//	String[] tab= {"ip0resized", "ip1resized","ip2resized","ip3resized","ip4resized","ip5resized","ip6resized"};
	
	/*ON VA STOCKER LES NIVEAUX DE GRIS DE CHAQUE PIXEL DE LA DERNIERE IMAGE : MARQUEUR NUCLEAIRE (IRIDIUM 191)
	 * DANS LA MATRICE MATPIXELNUC */
	int  getpixelnuc;
	int[][] matpixelnuc = new int[height1][height1];
	
	for(int i=0; i<height1; i++) {
		for(int j=0; j<height1; j++) {
			
			getpixelnuc = ip6resized.getPixel(i, j);
			matpixelnuc[i][j]=getpixelnuc;
			
		}	
	}
	/*AFFICHAGE MATRICE VALEURS NUANCES DE GRIS*/
	for(int i=0; i<height1; i++) {
		for(int j=0; j<height1; j++) {
			System.out.print(matpixelnuc[i][j]+" ");
		
		}
				System.out.println();
	}

	
	/* METHODE DU SEUIL (THRESHOLD) POUR SEPARER OBJET (NOYAUX) DU FOND :*/
	/* ON VA STOCKER DANS LA MATRICE IMAGE LES INDICES i j DE LA MATRICE MATPIXELNUC*/
	/* SUPERIEURS AU SEUIL (APPARTENANT AUX NOYAUX)*/
	
	/*ON VA STOCKER LES COORDONNEES DES NOYAUX DANS LA MATRICE IMAGE*/
	
	int[][] IMAGE = new int [height1][height1];
	for(int i=0; i<height1; i++) {
		for(int j=0; j<height1; j++) {	
			IMAGE[i][j]=0; }}
	
	for(int i=0; i<height1; i++) {
		for(int j=0; j<height1; j++) {		
			if(matpixelnuc[i][j]>=ip6resized.getAutoThreshold()) {
				IMAGE[i][j]=-1; //COULEUR BLANCHE POUR CES PIXELS (i,j)
				System.out.println(i+" "+j);
			}
		}
	}
	
	for(int a=0; a<height1; a++) {
		for(int b=0; b<height1; b++) {
			System.out.print(IMAGE[a][b]+" ");
		} 
		System.out.println();
	}
 
	/*TEST CONSTRUCTION D'UNE IMAGE A PARTIR DE LA MATRICE IMAGE*/
	
//	BufferedImage image;
//	try {
//		
//		 image = new BufferedImage(height1, height1, BufferedImage.TYPE_BYTE_BINARY);
//	    for(int c=0; c<height1; c++) {
//	        for(int d=0; d<height1; d++) {
//	        	
//	            int a = IMAGE[c][d];
//	           // Color newColor = new Color(a,a,a);
//	            image.setRGB(d,c,a);
//	           
//	        }
//	    }
//	    File output = new File("Grayscale.jpg");
//	    ImageIO.write(image, "jpg", output);
//	}
//
//	catch(Exception e) {}
    
	/*MAINTENANT ON VA RECUPERER LES VALEURS DES NIVEAUX DE GRIS SUR LES AUTRES IMAGES
	 * DE LA STACK QUI MARQUENT UN AUTRE COMPARTIMENT D'INTERET 
	 * ET DE RETOUR, STOCKER LES PIXELS APPARTENANT AU COMPARTIMENT D'INTERET EN QUESTION
	 * UNE FOIS CELA FAIT, ON FERA CORRESPONDRE LES 3 TABLEAUX STOCKANT LES PIXELS A 3 COULEURS
	 * DIFFERENTES ET ON CREERA UNE NOUVELLE IMAGE; QUI CORRESPONDRA A L'IMAGE DE LA STACK MAIS 
	 * SEGMENTEE SELON LE NOYAU/MEMBRANE/FOND */
	


	}	
	}
