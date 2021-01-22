import matplotlib.pyplot as plt
import matplotlib.image as mpimg


fig = plt.figure()
plt.subplots_adjust(wspace =0, hspace =0)

img_list = []

i = 1
for path in ['./', './']:
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
plt.show()
