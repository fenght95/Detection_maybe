import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img1 = mpimg.imread('./xml_demo/rgb/2-1_Z__000667.jpg')
img2 = mpimg.imread('./xml_demo/trm/2-1_Z__000667.jpg')
fig = plt.figure()
plt.subplots_adjust(wspace =0, hspace =0)

img_list = ['2-1_Z__000667', 'DJI_20201120201339_0003_Z__000088',
            'DJI_20201121164229_0004_Z__000078',
            'DJI_20201121164530_0005_Z__000132',
            'DJI_20201121172753_0006_Z__000245',
            'DJI_20201121173104_0007_Z__000369']

i = 1
for path in ['./xml_demo/', './']:
    for img in img_list:
        for xx in ['rgb', 'trm']:
            img1 = mpimg.imread(path + xx +'/' + img + '.jpg')
            if xx == 'trm':
                ax = fig.add_subplot(4, 6, i + 6)
            else:
                ax = fig.add_subplot(4, 6, i)
            ax.imshow(img1)
            plt.axis('off')

        i += 1
    i += 6



plt.savefig('./imshow.jpg')
#plt.show()
