# for cascade rcnn
import torch
import pdb
import collections
num_classes = 16

model_coco = torch.load('cascade_rcnn_r50_fpn_dconv_c3-c5_1x_coco_20200130-2f1fca44.pth')
'''
#pdb.set_trace()

# change model

# 'backbone.conv1.weight', 'backbone.bn1.weight', 'backbone.bn1.bias',
# 'backbone.bn1.running_mean', 'backbone.bn1.running_var', 'backbone.bn1.num_batches_tracked'
model_coco['state_dict']['backbone.conv1_34.weight'] = model_coco['state_dict']['backbone.conv1.weight']
model_coco['state_dict']['backbone.bn2.weight'] = model_coco['state_dict']['backbone.bn1.weight']
model_coco['state_dict']['backbone.bn2.bias'] = model_coco['state_dict']['backbone.bn1.bias']
model_coco['state_dict']['backbone.bn2.running_mean'] = model_coco['state_dict']['backbone.bn1.running_mean']
model_coco['state_dict']['backbone.bn2.running_var'] = model_coco['state_dict']['backbone.bn1.running_var']
model_coco['state_dict']['backbone.bn2.num_batches_tracked'] = model_coco['state_dict']['backbone.bn1.num_batches_tracked']

for i in range(1,5):
	if i == 1 or (i == 4):
		for j in range(3):
			for k in range(1,4):
				#pdb.set_trace()
				model_coco['state_dict']['backbone.layer%d.%d.conv%d.weight'%(i+6,j,k)] = model_coco['state_dict']['backbone.layer%d.%d.conv%d.weight'%(i,j,k)]
				for item in ['running_mean','running_var','weight','bias','num_batches_tracked']:
					model_coco['state_dict']['backbone.layer%d.%d.bn%d.'%(i+6,j,k) + item] = model_coco['state_dict']['backbone.layer%d.%d.bn%d.'%(i,j,k) + item]
		for item in ['running_mean','running_var','weight','bias','num_batches_tracked']:
			model_coco['state_dict']['backbone.layer%d.0.downsample.1.'%(i+6)+item]=model_coco['state_dict']['backbone.layer%d.0.downsample.1.'%i +item]
		model_coco['state_dict']['backbone.layer%d.0.downsample.0.weight'%(i+6)]=model_coco['state_dict']['backbone.layer%d.0.downsample.0.weight'%i]



	elif i == 2:
		for j in range(4):
			for k in range(1,4):
				#pdb.set_trace()
				model_coco['state_dict']['backbone.layer%d.%d.conv%d.weight'%(i+6,j,k)] = model_coco['state_dict']['backbone.layer%d.%d.conv%d.weight'%(i,j,k)]
				for item in ['running_mean','running_var','weight','bias','num_batches_tracked']:
					model_coco['state_dict']['backbone.layer%d.%d.bn%d.'%(i+6,j,k) + item] = model_coco['state_dict']['backbone.layer%d.%d.bn%d.'%(i,j,k) + item]
		model_coco['state_dict']['backbone.layer%d.0.downsample.0.weight'%(i+6)]=model_coco['state_dict']['backbone.layer%d.0.downsample.0.weight'%i]
		for item in ['running_mean','running_var','weight','bias','num_batches_tracked']:
			model_coco['state_dict']['backbone.layer%d.0.downsample.1.'%(i+6)+item]=model_coco['state_dict']['backbone.layer%d.0.downsample.1.'%i +item]
	elif i == 3:
		for j in range(6):
			for k in range(1,4):
				#pdb.set_trace()
				model_coco['state_dict']['backbone.layer%d.%d.conv%d.weight'%(i+6,j,k)] = model_coco['state_dict']['backbone.layer%d.%d.conv%d.weight'%(i,j,k)]
				for item in ['running_mean','running_var','weight','bias','num_batches_tracked']:
					model_coco['state_dict']['backbone.layer%d.%d.bn%d.'%(i+6,j,k) + item] = model_coco['state_dict']['backbone.layer%d.%d.bn%d.'%(i,j,k) + item]
		model_coco['state_dict']['backbone.layer%d.0.downsample.0.weight'%(i+6)]=model_coco['state_dict']['backbone.layer%d.0.downsample.0.weight'%i]
		for item in ['running_mean','running_var','weight','bias','num_batches_tracked']:
			model_coco['state_dict']['backbone.layer%d.0.downsample.1.'%(i+6)+item]=model_coco['state_dict']['backbone.layer%d.0.downsample.1.'%i +item]

'''
# weight
model_coco["state_dict"]["roi_head.bbox_head.0.fc_cls.weight"].resize_(num_classes,1024)
model_coco["state_dict"]["roi_head.bbox_head.1.fc_cls.weight"].resize_(num_classes,1024)
model_coco["state_dict"]["roi_head.bbox_head.2.fc_cls.weight"].resize_(num_classes,1024)
# bias
model_coco["state_dict"]["roi_head.bbox_head.0.fc_cls.bias"].resize_(num_classes)
model_coco["state_dict"]["roi_head.bbox_head.1.fc_cls.bias"].resize_(num_classes)
model_coco["state_dict"]["roi_head.bbox_head.2.fc_cls.bias"].resize_(num_classes)
#save new model
#pdb.set_trace()
torch.save(model_coco,"cas_classes_%d.pth"%num_classes)
